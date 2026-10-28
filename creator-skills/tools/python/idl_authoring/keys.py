"""Local identity authority for a new, course-free template."""
import argparse
import base64
from idl_backend.config import repository_root
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

def public_key_b64(fallback):
    path = repository_root() / "courses/identity-public-key.txt"
    return path.read_text(encoding="utf-8").strip() if path.exists() else fallback

def require_course_uuid():
    import os
    from idl_backend.contracts.courses import load_courses
    course = os.environ.get("IDL_COURSE_UUID", "")
    if course not in load_courses():
        raise ValueError("Set IDL_COURSE_UUID to a registered course UUID before generating assets.")
    return course

def main():
    argparse.ArgumentParser(description="Initialize a new template identity authority once.").parse_args()
    root = repository_root()
    private = root / "environment/backend/.private/module-identity-ed25519.pem"
    public = root / "courses/identity-public-key.txt"
    if private.exists() or public.exists() or any((root / "courses/modules").glob("*/outlines.json")):
        raise SystemExit("Refusing to replace keys or initialize over existing courses.")
    key = Ed25519PrivateKey.generate()
    private.parent.mkdir(parents=True, exist_ok=True)
    with private.open("xb") as stream:
        stream.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    with public.open("x", encoding="utf-8") as stream:
        stream.write(base64.b64encode(key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode() + "\n")
    print("Created template identity keys. Back up environment/backend/.private securely; never publish it.")

if __name__ == "__main__":
    main()
