#!.venv/bin/python3
import unittest
import pandas as pd
from classes import transform 

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

if __name__ == "__main__":
    unittest.main()