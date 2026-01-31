#!.dt-venv/bin/python3
import unittest
import pandas as pd
import dt.lib.transform as transform
import dt.io.reader as r
import dt.lib.filter as filter_lib

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

class TestFilters(unittest.TestCase):
    def test_from_dict(self):
        not_null_dict = {
            "type": "not_null",
            "column": "age"
        }

        regex_dict = {
            "type": "regex",
            "column": "code",
            "pattern": r"^[A-Z]{3}\d{3}$"
        }

        greater_than_dict = {
            "type": "greater_than",
            "column": "value",
            "threshold": 10
        }

        greater_than_equal_to_dict = {
            "type": "greater_than_equal_to",
            "column": "value",
            "threshold": 10
        }

        equal_to_dict = {
            "type": "equal_to",
            "column": "value",
            "threshold": 10
        }

        less_than_dict = {
            "type": "less_than",
            "column": "value",
            "threshold": 10
        }

        less_than_equal_to_dict = {
            "type": "less_than_equal_to",
            "column": "value",
            "threshold": 10
        }

        not_null_filter = filter_lib.FilterFactory.from_dict(not_null_dict)
        regex_filter = filter_lib.FilterFactory.from_dict(regex_dict)
        greater_than_filter = filter_lib.FilterFactory.from_dict(greater_than_dict)
        greater_than_equal_to_filter = filter_lib.FilterFactory.from_dict(greater_than_equal_to_dict)
        equal_to_filter = filter_lib.FilterFactory.from_dict(equal_to_dict)
        less_than_filter = filter_lib.FilterFactory.from_dict(less_than_dict)
        less_than_equal_to_filter = filter_lib.FilterFactory.from_dict(less_than_equal_to_dict)

        self.assertIsInstance(not_null_filter, filter_lib.NotNull)
        self.assertIsInstance(regex_filter, filter_lib.Regex)
        self.assertIsInstance(greater_than_filter, filter_lib.GreaterThan)
        self.assertIsInstance(greater_than_equal_to_filter, filter_lib.GreaterThanEqualTo)
        self.assertIsInstance(equal_to_filter, filter_lib.EqualTo)
        self.assertIsInstance(less_than_filter, filter_lib.LessThan)
        self.assertIsInstance(less_than_equal_to_filter, filter_lib.LessThanEqualTo)

    def test_NotNull(self):
        df = pd.DataFrame({
            "one": [1, None, 3],
            "two": [1, 2, 3]
        })

        filter = filter_lib.NotNull("one")

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([True, False, True])

        self.assertTrue(filteredSeries.equals(expectedSeries))

    def test_Regex(self):
        df = pd.DataFrame({
            "codes": ["ABC123", "DEF456", "hello", "JKL012"]
        })

        filter = filter_lib.Regex("codes", r"^[A-Z]{3}\d{3}$")

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([True, True, False, True])

        self.assertTrue(filteredSeries.equals(expectedSeries))

    def test_GreaterThan(self):
        df = pd.DataFrame({
            "values": [10, 20, 30, 40, 50]
        })

        filter = filter_lib.GreaterThan("values", 25)

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([False, False, True, True, True])

        self.assertTrue(filteredSeries.equals(expectedSeries))

    def test_GreaterThanEqualTo(self):
        df = pd.DataFrame({
            "values": [10, 20, 30, 40, 50]
        })

        filter = filter_lib.GreaterThanEqualTo("values", 30)

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([False, False, True, True, True])

        self.assertTrue(filteredSeries.equals(expectedSeries))

    def test_EqualTo(self):
        df = pd.DataFrame({
            "values": [10, 20, 30, 40, 50]
        })

        filter = filter_lib.EqualTo("values", 30)

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([False, False, True, False, False])

        self.assertTrue(filteredSeries.equals(expectedSeries))

    def test_LessThan(self):
        df = pd.DataFrame({
            "values": [10, 20, 30, 40, 50]
        })

        filter = filter_lib.LessThan("values", 30)

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([True, True, False, False, False])

        self.assertTrue(filteredSeries.equals(expectedSeries))

    def test_lessThanEqualTo(self):
        df = pd.DataFrame({
            "values": [10, 20, 30, 40, 50]
        })

        filter = filter_lib.LessThanEqualTo("values", 30)

        filteredSeries = filter.apply(df)
        expectedSeries = pd.Series([True, True, True, False, False])

        self.assertTrue(filteredSeries.equals(expectedSeries))

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