from pathlib import Path
import sys
import os
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "runtime/backend/src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools/python"))
# Only synthetic configuration for local tests; no request reaches a provider.
os.environ.setdefault("LLM_BASE_URL", "http://127.0.0.1:1")
os.environ.setdefault("LLM_API_KEY", "test-key")
os.environ.setdefault("LLM_MODEL", "test-model")
