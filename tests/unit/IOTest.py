import unittest
import pandas as pd
import beatmap as bt
from pathlib import Path

fixtures_path = Path(Path(__file__).parent.absolute(), "fixtures")


class TestIO(unittest.TestCase):
    def setup_class(self):
        # setting up test cases for import_data
        self.ok_test = {
            "file": Path(fixtures_path, "test_ok.csv"),
            "info": "test ok file",
            "a_o": 11.11,
        }

        # setting up empty file test
        self.empty_test = {
            "file": Path(fixtures_path, "test_empty.csv"),
            "info": "test empty file",
            "a_o": 11.11,
        }

        # setting up file with headers test
        self.header_test = {
            "file": Path(fixtures_path, "test_headers.csv"),
            "info": "test header file",
            "a_o": 11.11,
        }

        # setting up short test
        self.short_test = {
            "file": Path(fixtures_path, "test_short.csv"),
            "info": "test short file",
            "a_o": 11.11,
        }

        # setting up n equals zero test
        self.n_zero_test = {
            "file": Path(fixtures_path, "test_n0.csv"),
            "info": "test n0 file",
            "a_o": 11.11,
        }

        # setting up file with strings test
        self.strings_test = {
            "file": Path(fixtures_path, "test_strings.csv"),
            "info": "test strings file",
            "a_o": 11.11,
        }

        # setting up file not found test
        self.missing_file_test = {
            "file": Path(fixtures_path, "test_missing_file.csv"),
            "info": "test missing file",
            "a_o": 11.11,
        }

        # setting up .xlsx test
        self.xlsx_file_test = {
            "file": Path(fixtures_path, "test.xlsx"),
            "info": "test xlsx file",
            "a_o": 11.11,
        }

        # setting up a_o is a string test
        self.a_o_string_test = {
            "file": Path(fixtures_path, "test_ok.csv"),
            "info": "test ok file",
            "a_o": "11.11",
        }

        # setting up ok list import test
        self.list_data_test = {
            "relp": [0.1, 0.2, 0.21, 0.3, 0.4, 0.5],
            "n": [0.001, 0.002, 0.004, 0.005, 0.0055, 0.006],
            "file": "my file",
            "info": "my info",
            "a_o": 11.11,
        }

        # setting up not list like import test
        self.not_list_test = {
            "relp": 2,
            "n": 3,
            "file": "my file",
            "info": "my info",
            "a_o": 11.11,
        }

        # setting up incorrect size test
        self.bad_list_shape_test = {
            "relp": [[0.1, 0.2, 0.21, 0.3, 0.4, 0.5], [0.1, 0.2, 0.21, 0.3, 0.4, 0.5]],
            "n": [0.001, 0.002, 0.004, 0.005, 0.0055, 0.006],
            "file": "my file",
            "info": "my info",
            "a_o": 11.11,
        }

        # setting up a_o not numeric test
        self.ao_not_numeric_list_test = {
            "relp": [0.1, 0.2, 0.21, 0.3, 0.4, 0.5],
            "n": [0.001, 0.002, 0.004, 0.005, 0.0055, 0.006],
            "file": "my file",
            "info": "my info",
            "a_o": "cat",
        }

    def test_import_data(self):
        # test ok data file
        temp = bt.io.import_data(**self.ok_test)
        assert temp.iso_df.equals(bt.io.import_data(**self.ok_test).iso_df)
        assert temp.file == self.ok_test["file"]
        assert temp.info == self.ok_test["info"]
        assert temp.a_o == self.ok_test["a_o"]

        # test empty data file
        with self.assertRaises(pd.errors.EmptyDataError):
            bt.io.import_data(**self.empty_test)

        # test data file with headers

        temp = bt.io.import_data(**self.header_test)
        assert temp.iso_df.equals(bt.io.import_data(**self.header_test).iso_df)
        assert temp.file == self.header_test["file"]
        assert temp.info == self.header_test["info"]
        assert temp.a_o == self.header_test["a_o"]

        # test short datafile
        with self.assertRaises(TypeError):
            bt.io.import_data(**self.short_test)

        # test n equals zero datafile
        with self.assertRaises(ValueError):
            bt.io.import_data(**self.n_zero_test)

        # test file not found
        with self.assertRaises(FileNotFoundError):
            bt.io.import_data(**self.missing_file_test)

        # test xlsx data file
        with self.assertRaises(UnicodeDecodeError):
            bt.io.import_data(**self.xlsx_file_test)

        # test a_o is a string
        with self.assertRaises(ValueError):
            bt.io.import_data(**self.a_o_string_test)

    def test_import_list_data(self):
        # test ok lists
        temp = bt.io.import_list_data(**self.list_data_test)
        assert temp.iso_df.equals(bt.io.import_list_data(**self.list_data_test).iso_df)

        # test not list like
        with self.assertRaises(ValueError):
            bt.io.import_list_data(**self.not_list_test)

        # test bad list shape
        with self.assertRaises(ValueError):
            bt.io.import_list_data(**self.bad_list_shape_test)

        # test non numeric a_o
        with self.assertRaises(ValueError):
            bt.io.import_list_data(**self.ao_not_numeric_list_test)


if __name__ == "__main__":

    t = TestIO()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith("test"):
            print("running test: " + item)
            t.__getattribute__(item)()
