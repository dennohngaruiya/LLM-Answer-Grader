"""Tests for the scorer. Run with:  python -m unittest discover -s tests -v"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from grader.scorer import evaluate, grade_for, _fenced_json  # noqa: E402


class TestGrades(unittest.TestCase):
    def test_grade_boundaries(self):
        self.assertEqual(grade_for(100), "A")
        self.assertEqual(grade_for(90), "A")
        self.assertEqual(grade_for(89.9), "B")
        self.assertEqual(grade_for(70), "C")
        self.assertEqual(grade_for(60), "D")
        self.assertEqual(grade_for(59.9), "F")


class TestJsonHandling(unittest.TestCase):
    def test_fenced_json_is_parsed(self):
        raw = "```json\n{\"a\": 1}\n```"
        self.assertEqual(json.loads(_fenced_json(raw)), {"a": 1})

    def test_missing_key_is_penalised(self):
        card = evaluate({"id": "t", "prompt": "p", "answer": "{\"a\": 1}",
                         "expected_format": "json", "required_keys": ["a", "b"]})
        fmt = next(d for d in card.dimensions if d.id == "format")
        self.assertLess(fmt.score, 5)
        self.assertTrue(any("b" in f.message for f in fmt.findings))

    def test_invalid_json_scores_zero_format(self):
        card = evaluate({"id": "t", "prompt": "p", "answer": "not json at all",
                         "expected_format": "json", "required_keys": ["a"]})
        fmt = next(d for d in card.dimensions if d.id == "format")
        self.assertEqual(fmt.score, 0.0)


class TestGrounding(unittest.TestCase):
    def test_unsupported_number_is_flagged(self):
        card = evaluate({
            "id": "g", "prompt": "p",
            "source": "Refunds take 14 days.",
            "answer": "Refunds take 3 days and we handled 1.2 million cases.",
        })
        ground = next(d for d in card.dimensions if d.id == "grounding")
        self.assertLess(ground.score, 5)
        self.assertTrue(any(f.severity == "medium" for f in ground.findings))

    def test_no_source_is_not_penalised(self):
        card = evaluate({"id": "g", "prompt": "p", "answer": "Anything at all."})
        ground = next(d for d in card.dimensions if d.id == "grounding")
        self.assertEqual(ground.score, 5.0)


class TestSafety(unittest.TestCase):
    def test_script_tag_is_high_severity(self):
        card = evaluate({"id": "s", "prompt": "p", "answer": "<script>alert(1)</script> hi"})
        safety = next(d for d in card.dimensions if d.id == "safety")
        self.assertTrue(any(f.severity == "high" for f in safety.findings))
        self.assertLess(safety.score, 5)

    def test_forbidden_element_hits_adherence(self):
        card = evaluate({"id": "s", "prompt": "p", "answer": "password is Hunter2",
                         "must_not_include": ["password is"]})
        adh = next(d for d in card.dimensions if d.id == "adherence")
        self.assertTrue(any(f.severity == "high" for f in adh.findings))


class TestEndToEnd(unittest.TestCase):
    def test_sample_file_produces_cards_with_grades(self):
        cases = json.loads(Path(__file__).resolve().parents[1].joinpath("data/sample_outputs.json").read_text())
        cards = [evaluate(c) for c in cases]
        self.assertEqual(len(cards), len(cases))
        for c in cards:
            self.assertIn(c.grade, "ABCDF")
            self.assertGreaterEqual(c.total, 0)
            self.assertLessEqual(c.total, 100)

    def test_scores_are_deterministic(self):
        case = {"id": "d", "prompt": "p", "answer": "Same input, same output."}
        self.assertEqual(evaluate(case).total, evaluate(case).total)


if __name__ == "__main__":
    unittest.main()
