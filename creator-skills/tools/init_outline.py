"""Create only a missing template outline; never overwrite an existing course."""
import argparse
import json
import os
from pathlib import Path
import re
import tempfile


def ensure_outline(repository, directory, title=None, dry_run=False):
    root = Path(repository).resolve()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", directory):
        raise ValueError("Use a single module directory name")
    modules = (root / "courses/modules").resolve()
    target = modules / directory
    if not modules.is_relative_to(root) or target.is_symlink() or target.resolve().parent != modules:
        raise ValueError("Module must remain under courses/modules")
    outline = target / "outlines.json"
    if outline.is_symlink():
        raise ValueError("Outline must not be a symbolic link")
    if outline.exists():
        if not outline.is_file():
            raise ValueError("Outline must be a regular file")
        return {"status": "unchanged", "path": str(outline)}
    if title is not None and not title.strip():
        raise ValueError("Title must not be empty")
    if dry_run:
        return {"status": "would-create", "path": str(outline)}
    document = {"id": directory.lower(), "title": title or directory, "description": "",
                "path": "/modules/" + directory.lower(), "pages": []}
    target.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=target,
                                         prefix=".outlines-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(document, stream, ensure_ascii=False, indent=2)
            stream.write("\n");stream.flush();os.fsync(stream.fileno())
        try:
            os.link(temporary, outline)
        except FileExistsError:
            if outline.is_symlink() or not outline.is_file():
                raise ValueError("Outline must be a regular file")
            return {"status": "unchanged", "path": str(outline)}
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
    return {"status": "created", "path": str(outline),
            "next": "Sign the new outline with the existing idl_authoring.identity tool before preview."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True)
    parser.add_argument("--title")
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result = ensure_outline(args.repository, args.directory, args.title, args.dry_run)
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
