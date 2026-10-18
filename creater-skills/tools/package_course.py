#!/usr/bin/env python3
"""Build a portable classroom locally, then zip the complete courses snapshot."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]

def package(root=ROOT, build=True):
    root = Path(root)
    courses = root / "courses"
    manifest_file = courses / "shuku.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if build:
        subprocess.run(["npm.cmd" if os.name == "nt" else "npm", "--prefix", str(root / "environment/frontend"), "run", "build"], cwd=root, env={**os.environ, "SHUKU_EXPORT": "1", "VITE_ENABLE_TELEMETRY": "false", "VITE_ASSET_BASE_URL": ""}, check=True)
        built = root / "runtime/data/build/frontend"
        if not (built / "index.html").is_file():
            raise ValueError("未生成预览入口")
        preview = courses / "preview"
        if preview.exists():
            shutil.rmtree(preview)
        shutil.copytree(built, preview)
        manifest["preview"] = {"entry": "preview/index.html"}
        manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not build:
        manifest.pop("preview", None)
    files = sorted(file for file in courses.rglob("*") if file.is_file() and (build or file.relative_to(courses).parts[0] != "preview"))
    if any(file.is_symlink() for file in courses.rglob("*")):
        raise ValueError("课程不能包含符号链接")
    if len(files) > 1000 or sum(file.stat().st_size for file in files) > 100 * 1024 * 1024:
        raise ValueError("课程超过 1000 文件或 100 MiB")
    archive = root / "course.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as zipped:
        for file in files:
            if file == manifest_file and not build:
                zipped.writestr("shuku.json", json.dumps(manifest, ensure_ascii=False))
            else:
                zipped.write(file, file.relative_to(courses).as_posix())
    if archive.stat().st_size > 100 * 1024 * 1024:
        archive.unlink()
        raise ValueError("ZIP 超过 100 MiB")
    return archive

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-only", action="store_true", help="仅保存源码阶段，不生成预览")
    args = parser.parse_args()
    print(package(build=not args.source_only))
