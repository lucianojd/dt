import pandas as pd
from abc import ABC, abstractmethod
from enum import Enum

class Filter(ABC):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

class NotNull(Filter):
    def __init__(self, column: str | int):
        super().__init__()
        self.column = column

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].notnull()
    
    def __str__(self) -> str:
        return f"NotNull(column={self.column})"

class GreaterThan(Filter):
    def __init__(self, column: str | int, threshold: int | float):
        super().__init__()
        self.column = column
        self.threshold = threshold

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] > self.threshold
    
    def __str__(self) -> str:
        return f"GreaterThan(column={self.column}, threshold={self.threshold})"

class FilterType(Enum):
    NOT_NULL = "not_null"
    GREATER_THAN = "greater_than"

class FilterFactory:
    @staticmethod
    def from_dict(f_dict: dict) -> Filter:
        f_type = FilterType(f_dict.get("type"))
        match f_type:
            case FilterType.NOT_NULL:
                column = f_dict.get("column")
                if isinstance(column, (int, str)):
                    return NotNull(column)
                else:
                    raise ValueError("NotNull filter requires a string or integer column identifier.")
            case FilterType.GREATER_THAN:
                column = f_dict.get("column")
                threshold = f_dict.get("threshold")

                if isinstance(column, (int, str)) and isinstance(threshold, (int, float)):
                    return GreaterThan(column, threshold)
                else:
                    raise ValueError("GreaterThan filter requires a string or integer column identifier and a numeric threshold.")
            case _:
                raise ValueError(f"Filter type not supported: {f_type}")