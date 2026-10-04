"""Regression: T1 notes document SB 763 gap and fail-closed reading."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class T1NotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.changes = json.loads((ROOT / "output" / "changes.json").read_text())
    def test_t1_mentions_sb763_as_unresolved_research_gap(self):
        notes = self.changes["T1"]["notes"]
        self.assertIn("SB 763", notes)
        self.assertIn("unresolved_source_gap", notes)
        self.assertIn("research_task", notes)
    def test_t1_explains_failclosed_unknown_instead_of_applies(self):
        t1 = self.changes["T1"]
        self.assertEqual(t1["affected_address_ids"], [])
        self.assertTrue(t1["hypothetically_affected_address_ids"])
        notes = t1["notes"]
        for token in ("jurisdiction is established", "in force after 2026-01-01", "only missing documented property facts", "hypothetically_affected", "not_yet_effective-to-unknown", "never promotes unknown to applies"):
            self.assertIn(token, notes)
if __name__ == "__main__":
    unittest.main()
