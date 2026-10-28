from pathlib import Path
import importlib.util
import json
import subprocess
import sys
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "creator-skills"


def tool(name):
    spec = importlib.util.spec_from_file_location("template_" + name, SKILL / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_renamed_skill_and_tool_configuration_have_real_targets():
    assert SKILL.is_dir() and not (ROOT / ("creater" + "-skills")).exists()
    assert (SKILL / "SKILL.md").read_text(encoding="utf-8").startswith("---\nname: creator-skills\n")
    for group in ("frontend", "agent-demo"):
        package = json.loads((ROOT / "environment" / group / "package.json").read_text())
        for command in package["scripts"].values():
            assert "creater" + "-skills" not in command
    manifest = json.loads((SKILL / "integration/skill.manifest.json").read_text())
    for stage in ("bootstrap", "validate", "stop"):
        args = manifest["lifecycle"][stage]["args"]
        assert (ROOT / args[-1]).is_file()
    for positive in (SKILL / "assets/visual_samples").glob("pos_*.jpg"):
        assert positive.with_name(positive.name.replace("pos_", "neg_", 1)).is_file()
    assert len(list((SKILL / "assets/visual_samples").glob("pos_*.jpg"))) >= 5


def test_outline_initialization_is_nondestructive_and_does_not_prebuild_pages(tmp_path):
    init = tool("init_outline")
    assert init.ensure_outline(tmp_path, "Lesson", dry_run=True)["status"] == "would-create"
    assert not (tmp_path / "courses").exists()
    assert init.ensure_outline(tmp_path, "Lesson", "课程🙂")["status"] == "created"
    target = tmp_path / "courses/modules/Lesson"
    document = json.loads((target / "outlines.json").read_text())
    assert document["pages"] == [] and document["path"] == "/modules/lesson"
    assert "moduleIdentity" not in document
    assert list(target.iterdir()) == [target / "outlines.json"]
    # Existing content, even non-JSON work in progress, must never be overwritten.
    (target / "outlines.json").write_bytes(b"unfinished-user-content")
    assert init.ensure_outline(tmp_path, "Lesson", "Other")["status"] == "unchanged"
    assert (target / "outlines.json").read_bytes() == b"unfinished-user-content"


@pytest.mark.parametrize("name", ["../escape", "/absolute", r"a\b", "a/b", ""])
def test_outline_initialization_rejects_path_escapes(tmp_path, name):
    with pytest.raises(ValueError):tool("init_outline").ensure_outline(tmp_path, name)
    assert not (tmp_path / "courses").exists()


def test_outline_initialization_rejects_symlink_escape(tmp_path):
    root=tmp_path / "root";outside=tmp_path / "outside";root.mkdir();outside.mkdir()
    (root / "courses").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):tool("init_outline").ensure_outline(root, "Lesson")
    assert list(outside.iterdir()) == []


def test_course_archive_excludes_module_and_page_scratchpads(tmp_path):
    courses = tmp_path / "courses";courses.mkdir()
    (courses / "shuku.json").write_text('{"courseKey":"keep-course-key"}')
    files = {"modules/Lesson/Lesson.tsx": "course-source",
             "modules/Lesson/_scratchpad/original.txt": "not-for-publication",
             "modules/Lesson/pages/Opening/_scratchpad/prompt.txt": "private-prompt",
             "assets/example.svg": "<svg/>"}
    for name, content in files.items():
        path=courses / name;path.parent.mkdir(parents=True, exist_ok=True);path.write_text(content)
    with ZipFile(tool("package_course").package(tmp_path, build=False)) as archive:
        assert set(archive.namelist()) == {"shuku.json", "modules/Lesson/Lesson.tsx", "assets/example.svg"}
        assert json.loads(archive.read("shuku.json"))["courseKey"] == "keep-course-key"


def test_initializer_cli_works_without_backend_dependencies(tmp_path):
    result = subprocess.run([sys.executable, str(SKILL / "tools/init_outline.py"), "--repository", str(tmp_path),
                             "--directory", "NewCourse", "--title", "新课程"], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "created"
