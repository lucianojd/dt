#!.dt-venv/bin/python3
import unittest
import pandas as pd
import dt.lib.transform as transform
import dt.io.reader as r

class TestTransforms(unittest.TestCase):
    def test_TrimStrings(self):
        df = pd.DataFrame({
            "name": [" Obi-wan ", " Anakin   ", "Count Dooku"],
        })

        expected_df = pd.DataFrame({
            "name": ["Obi-wan", "Anakin", "Count Dooku"],
        })

        t = transform.TrimStrings(columns=["name"])
        t_df = t.transform(df)

        self.assertTrue(t_df.equals(expected_df))

    def test_RenameColumns(self):
        df = pd.DataFrame({
            "old_name": [1, 2, 3],
        })

        expected_df = pd.DataFrame({
            "new_name": [1, 2, 3],
        })

        t = transform.RenameColumns(columns={"old_name": "new_name"})
        t_df = t.transform(df)

        self.assertTrue(t_df.equals(expected_df))

class TestCSVReader(unittest.TestCase):
    def test_ReadSingleCSV(self):
        df = r.DataReader("tests/data/test.csv", True, False).read()
        expected_df = pd.DataFrame({
            "name": ["transaction1", "transaction2", "transaction3"],
            "date": ["2025-01-01", "2025-02-02", "2025-03-03"],
            "amount": [10.00, 20.00, 30.00]
        })

        self.assertTrue(df.equals(expected_df))

    def test_ReadMultipleCSV(self):
        df = r.DataReader("tests/data/multiple_csvs", True, False).read()
        expected_df = pd.DataFrame({
            "name": ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9"],
            "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-02-01", "2025-02-02", "2025-02-03", "2025-03-01", "2025-03-02", "2025-03-03"],
            "amount": [1.0,2.0,3.0,10.0,20.0,30.0,100.0,200.0,300.0]
        })

        self.assertTrue(df.equals(expected_df))

class TestConfigReader(unittest.TestCase):
    def test_ConfigDescription(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()