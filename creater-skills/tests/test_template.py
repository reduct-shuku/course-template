import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def test_new_authority_can_sign_validate_and_reject_tampering(tmp_path):
    (tmp_path / "courses/modules").mkdir(parents=True)
    env = {**os.environ, "IDL_REPOSITORY_ROOT": str(tmp_path), "PYTHONUTF8": "1"}

    def run(module, *arguments):
        return subprocess.run([sys.executable, "-m", module, *arguments], env=env, capture_output=True, text=True, encoding="utf-8")

    assert run("idl_authoring.keys").returncode == 0
    assert run("idl_authoring.keys").returncode != 0
    course = tmp_path / "courses/modules/TestCourse"
    course.mkdir()
    outline = course / "outlines.json"
    outline.write_text(json.dumps({"id": "test-course", "path": "/modules/testcourse"}), encoding="utf-8")
    assert run("idl_authoring.identity").returncode == 0
    assert run("idl_authoring.identity", "--check").returncode == 0
    registered = run("idl_backend", "courses")
    assert registered.returncode == 0 and "test-course" in registered.stdout
    content = json.loads(outline.read_text(encoding="utf-8"))
    content["moduleIdentity"]["id"] = "2e5c4732-a40a-4d20-b954-a61507aabc75"
    outline.write_text(json.dumps(content), encoding="utf-8")
    assert run("idl_authoring.identity", "--check").returncode != 0
    assert run("idl_backend", "courses").returncode != 0


def test_inline_question_does_not_depend_on_a_bundled_bank(monkeypatch):
    from idl_backend.assessment.tasks import short_answer
    def forbidden_bank():
        raise AssertionError("Inline evaluation must not read a bundled bank")
    monkeypatch.setattr(short_answer, "load_question_bank", forbidden_bank)
    monkeypatch.setattr(short_answer, "run_structured", lambda **kwargs: kwargs["variables"])
    result = short_answer.evaluate_short_answer({"question": "What is 1 + 1?", "reference_answer": "2", "answer": "2"}, 1)
    assert result["question"] == "What is 1 + 1?"
    assert result["reference_answer"] == "- 2"
    assert result["task_id"].startswith("inline:")

