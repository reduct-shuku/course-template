from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from idl_backend.assessment.precomputed_cache import (
    CacheValidationError,
    VersionedJsonCache,
    atomic_write_json,
    normalize_cache_key,
    validate_cache_document,
)
from idl_backend.assessment.tasks.decision import analyze_decision_intake, generate_extra_decision_factors


def document(status: str = "approved") -> dict[str, object]:
    return {
        "schema_version": 1,
        "namespace": "decision-candidates",
        "content_version": 1,
        "generator": {"id": "test"},
        "entries": [{
            "id": "decision-001",
            "key": "读研",
            "aliases": ["考研究生"],
            "outputs": {
                "intake": {
                    "status": "ok",
                    "decision": "要不要读研？",
                    "positive_label": "读研",
                    "negative_label": "不读研",
                    "primary_factor": {"name": "研究兴趣"},
                },
                "extra_factors": {"factors": [{"name": "职业发展"}, {"name": "经济压力"}]},
            },
            "review": {"status": status},
        }],
    }


class VersionedJsonCacheTests(unittest.TestCase):
    def test_only_approved_entries_are_served_and_results_are_copied(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "decision-candidates.json"
            atomic_write_json(path, document())
            cache = VersionedJsonCache("decision-candidates", root=root)
            first = cache.lookup("要不要考研究生？")
            self.assertIsNotNone(first)
            first["outputs"] = {}
            self.assertIn("intake", cache.lookup("读研")["outputs"])

            atomic_write_json(path, document("generated"))
            self.assertIsNone(cache.lookup("读研"))

    def test_duplicate_normalized_alias_is_rejected(self) -> None:
        invalid = document()
        invalid["entries"][0]["aliases"] = ["考研究生", "要不要考研究生？"]
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(CacheValidationError):
            atomic_write_json(Path(directory) / "decision-candidates.json", invalid)


class DecisionCacheRouteTests(unittest.TestCase):
    def test_intake_cache_hit_does_not_call_model(self) -> None:
        cached = {"status": "ok", "decision": "要不要读研？"}
        with patch("idl_backend.assessment.tasks.decision.cached_decision_intake", return_value=cached), patch(
            "idl_backend.assessment.tasks.decision.generate_decision_intake_uncached"
        ) as uncached:
            self.assertEqual(analyze_decision_intake({"decision": "读研"}, 1.0), cached)
            uncached.assert_not_called()

    def test_extra_factor_cache_hit_does_not_call_model(self) -> None:
        cached = {"factors": [{"name": "A"}, {"name": "B"}]}
        with patch("idl_backend.assessment.tasks.decision.cached_extra_decision_factors", return_value=cached), patch(
            "idl_backend.assessment.tasks.decision.generate_extra_decision_factors_uncached"
        ) as uncached:
            self.assertEqual(generate_extra_decision_factors({"decision": "要不要读研？"}, 1.0), cached)
            uncached.assert_not_called()


class EmptyTemplateCacheTests(unittest.TestCase):
    def test_no_precomputed_answers_are_bundled(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = VersionedJsonCache("decision-candidates", root=Path(directory))
            self.assertIsNone(cache.lookup("any question"))
            self.assertEqual(cache.status()["entries"], 0)

if __name__ == "__main__":
    unittest.main()
