"""Verify calendar interpretation and last-good-snapshot safety without network."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import update_github


def calendar_html(label="2 contributions on January 1st."):
    return "".join(
        f'<td id="day-{i}" data-date="2026-{i // 28 + 1:02d}-{i % 28 + 1:02d}" '
        f'data-level="1"></td><tool-tip for="day-{i}">{label}</tool-tip>'
        for i in range(350)
    )


class CalendarTests(unittest.TestCase):
    def test_counts_come_from_tooltips_not_colour_levels(self):
        parser = update_github.Calendar()
        parser.feed(calendar_html())
        self.assertEqual(sum(day["count"] for day in parser.days()), 700)
        self.assertEqual(parser.days()[0]["level"], 1)

    def test_empty_calendar_is_rejected(self):
        with self.assertRaises(ValueError):
            update_github.Calendar().days()

    def test_missing_counts_are_rejected_instead_of_inventing_zero(self):
        parser = update_github.Calendar()
        parser.feed(calendar_html("Unexpected markup"))
        with self.assertRaises(ValueError):
            parser.days()

    def test_zero_is_parsed(self):
        parser = update_github.Calendar()
        parser.feed(calendar_html("No contributions on January 1st."))
        self.assertEqual(sum(day["count"] for day in parser.days()), 0)

    def test_failed_refresh_preserves_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets").mkdir()
            snapshot = root / "assets/github-stats.json"
            snapshot.write_text('{"lastGood":true}', encoding="utf-8")
            responses = [json.dumps({"login": "test"}), "[]", "changed markup"]
            with patch.object(update_github, "ROOT", root), patch.object(update_github, "get", side_effect=responses):
                with self.assertRaises(ValueError):
                    update_github.main()
            self.assertEqual(json.loads(snapshot.read_text()), {"lastGood": True})


if __name__ == "__main__":
    unittest.main()
