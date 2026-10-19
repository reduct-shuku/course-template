import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]


class UploadGuideTest(unittest.TestCase):
    def test_contribution_preview_is_committable_and_uses_fork_workflow(self):
        guide = (ROOT / "creater-skills/collaboration/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("个人工作分支", guide)
        self.assertIn("courses/preview/", guide)
        self.assertIn("不调用阶段版本上传接口", guide)
        self.assertIn("package_course.py", guide)
        self.assertNotIn("/courses/preview/", (ROOT / ".gitignore").read_text())

    def test_documented_upload_and_query_use_local_token_and_file_only(self):
        guide = (ROOT / "UPLOAD.md").read_text(encoding="utf-8")
        commands = re.findall(r"```bash\n(.*?)\n```", guide, re.S)
        self.assertEqual(len(commands), 2)
        requests = []

        class Handler(BaseHTTPRequestHandler):
            def handle_request(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                requests.append((self.command, self.path, dict(self.headers), body))
                result = ({"taskId": "guide-task", "status": "queued"} if self.command == "POST"
                          else {"taskId": "guide-task", "status": "succeeded", "result": {"previewUrl": "/preview/guide"}})
                self.send_response(202 if self.command == "POST" else 200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())

            do_POST = handle_request
            do_GET = handle_request

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                (directory / "api_token").write_text("example-local-token\r\n", encoding="utf-8")
                (directory / "course.zip").write_bytes(b"example-course-zip")
                env = {**os.environ, "SHUKU_URL": f"http://127.0.0.1:{server.server_port}",
                       "TASK_ID": "guide-task", "UPLOAD_ID": "guide-upload-uuid"}
                for command in commands:
                    response = subprocess.run(["bash", "-c", command], cwd=directory, env=env,
                                              capture_output=True, text=True, timeout=15, check=True)
                    self.assertEqual(json.loads(response.stdout)["taskId"], "guide-task")
            self.assertEqual([r[:2] for r in requests], [
                ("POST", "/api/agent/courses/upload"), ("GET", "/api/agent/tasks/guide-task")])
            for request in requests:
                self.assertEqual(request[2]["Authorization"], "Bearer example-local-token")
            self.assertEqual(requests[0][2]["Idempotency-Key"], "guide-upload-uuid")
            self.assertIn(b'name="file"', requests[0][3])
            self.assertIn(b"example-course-zip", requests[0][3])
            self.assertNotIn(b"example-local-token", requests[0][3])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_documented_package_contains_courses_content_without_repository_files(self):
        guide = (ROOT / "UPLOAD.md").read_text(encoding="utf-8")
        programs = re.findall(r"```python\n(.*?)\n```", guide, re.S)
        self.assertEqual(len(programs), 1)
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            files = {"courses/shuku.json": '{"schema_version":1}',
                     "courses/modules/Demo/README.md": "course notes",
                     "courses/modules/Demo/Lesson.tsx": "export default function Lesson() {}",
                     "courses/assets/example.svg": "<svg/>",
                     "api_token": "example-local-token", "environment/config.json": "{}",
                     "runtime/start.ps1": "runtime", ".git/config": "git metadata"}
            for name, content in files.items():
                target = directory / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            subprocess.run(["python3", "-c", programs[0]], cwd=directory, check=True, timeout=15)
            with ZipFile(directory / "course.zip") as package:
                self.assertEqual(set(package.namelist()), {
                    "shuku.json", "modules/Demo/README.md", "modules/Demo/Lesson.tsx", "assets/example.svg"})
                self.assertEqual(package.read("modules/Demo/README.md"), b"course notes")
        self.assertIn("不要求 HTML 入口", guide)
        self.assertIn("不限制 React/TSX", guide)
        self.assertIn("sourceOnly: true", guide)

    def test_local_build_packages_source_and_preview_and_updates_manifest(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location("package_course", ROOT / "creater-skills/tools/package_course.py")
        tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tool)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, content in {"courses/shuku.json": '{"courseKey":"keep-me","entry":"SKILL.md"}',
                                  "courses/modules/Lesson.tsx": "source", "api_token": "private",
                                  "runtime/data/build/frontend/index.html": '<script src="./assets/app.js"></script>',
                                  "runtime/data/build/frontend/assets/app.js": "built"}.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            with patch.object(tool.subprocess, "run") as build:
                archive = tool.package(root)
                self.assertEqual(build.call_args.kwargs["env"]["SHUKU_EXPORT"], "1")
            manifest = json.loads((root / "courses/shuku.json").read_text())
            self.assertEqual(manifest["courseKey"], "keep-me")
            self.assertEqual(manifest["entry"], "SKILL.md")
            self.assertEqual(manifest["preview"], {"entry": "preview/index.html"})
            with ZipFile(archive) as package:
                self.assertEqual(set(package.namelist()), {"shuku.json", "modules/Lesson.tsx", "preview/index.html", "preview/assets/app.js"})
            source_archive = tool.package(root, build=False)
            with ZipFile(source_archive) as source:
                self.assertNotIn("preview/index.html", source.namelist())
                self.assertNotIn("preview", json.loads(source.read("shuku.json")))
            with patch.object(tool.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "npm")):
                with self.assertRaises(subprocess.CalledProcessError):
                    tool.package(root)

    def test_token_file_is_ignored_and_guide_is_discoverable(self):
        ignored = subprocess.run(["git", "check-ignore", "--no-index", "api_token"],
                                 cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(ignored.stdout.strip(), "api_token")
        self.assertIn("(UPLOAD.md)", (ROOT / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
