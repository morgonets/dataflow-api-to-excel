"""Check Excel export using mocked API data, without internet access."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from openpyxl import load_workbook

import dataflow


class ExcelExportTests(unittest.TestCase):
    def setUp(self):
        self.users = [{
            "id": 1,
            "name": "Alice Smith",
            "username": "alice",
            "email": "alice@example.com",
            "phone": "0123-456-789",
            "website": "alice.example.com",
            "address": {"city": "Warsaw"},
            "company": {"name": "Example Company"},
        }]

    @patch("dataflow.requests.get")
    def test_exports_columns_values_and_formatting(self, get):
        get.return_value.json.return_value = self.users
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "users.xlsx"
            with patch("dataflow.OUTPUT_FILE", filename), redirect_stdout(io.StringIO()):
                self.assertEqual(dataflow.main(), 0)

            get.assert_called_once_with(dataflow.USERS_URL, timeout=10)
            get.return_value.raise_for_status.assert_called_once_with()
            workbook = load_workbook(filename)
            try:
                sheet = workbook["Users"]
                self.assertEqual(list(sheet.values), [
                    ("ID", "Name", "Username", "Email", "Phone", "Website", "City", "Company"),
                    (1, "Alice Smith", "alice", "alice@example.com", "0123-456-789",
                     "alice.example.com", "Warsaw", "Example Company"),
                ])
                self.assertTrue(all(cell.font.bold for cell in sheet[1]))
                for column in sheet.columns:
                    longest = max(len(str(cell.value)) for cell in column)
                    width = sheet.column_dimensions[column[0].column_letter].width
                    self.assertGreaterEqual(width, longest + 2)
            finally:
                workbook.close()

    @patch("dataflow.Workbook.save", side_effect=PermissionError("Permission denied"))
    @patch("dataflow.requests.get")
    def test_reports_file_writing_error(self, get, save):
        get.return_value.json.return_value = self.users
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            self.assertEqual(dataflow.main(), 1)
        save.assert_called_once_with("users.xlsx")
        self.assertIn("Could not write Excel file 'users.xlsx'", stderr.getvalue())
        self.assertIn("Permission denied", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
