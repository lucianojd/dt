import pandas as pd
from abc import ABC, abstractmethod
from enum import Enum

class Filter(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, f_dict: dict) -> Filter:
        pass

    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class FilterError(ValueError):
    def __init__(self, filter: str, message: str):
        super().__init__(f"{filter} filter error {message}")

class NotNull(Filter):
    """Filter for checking that a column is not null"""
    def __init__(self, column: str | int):
        super().__init__()
        self.column = column

    @classmethod
    def from_dict(cls, f_dict: dict) -> NotNull:
        column = f_dict.get("column")
        if isinstance(column, (int, str)):
            return cls(column)
        else:
            raise FilterError("NotNull", f"column {column} is not a valid string or integer")

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].notnull()
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(column={self.column})"
    

class Regex(Filter):
    """Filter for checking that a column matches a regex pattern"""
    def __init__(self, column: str | int, pattern: str):
        super().__init__()
        self.column = column
        self.pattern = pattern

    @classmethod
    def from_dict(cls, f_dict: dict) -> Regex:
        column = f_dict.get("column")
        pattern = f_dict.get("pattern")
        if isinstance(column, (int, str)) and isinstance(pattern, str):
            return cls(column, pattern)
        else:
            raise FilterError("Regex", f"column {column} or pattern {pattern} are not valid types")

    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].astype(str).str.match(self.pattern)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(column={self.column}, pattern={self.pattern})"


class ComparisonFilter(Filter):
    def __init__(self, column: str | int, threshold: int | float):
        super().__init__()
        self.column = column
        self.threshold = threshold

    @classmethod
    def from_dict(cls,f_dict: dict) -> ComparisonFilter:
        column = f_dict.get("column")
        threshold = f_dict.get("threshold")
        if isinstance(column, (int, str)) and isinstance(threshold, (int, float)):
            return cls(column, threshold)
        else:
            raise FilterError(cls.__name__, f"column {column} or threshold {threshold} are not valid types")
    
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.Series:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(column={self.column}, threshold={self.threshold})"

class GreaterThan(ComparisonFilter):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] > self.threshold
    
class GreaterThanEqualTo(ComparisonFilter):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] >= self.threshold

class EqualTo(ComparisonFilter):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] == self.threshold

class LessThan(ComparisonFilter):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] < self.threshold

class LessThanEqualTo(ComparisonFilter):
    def apply(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] <= self.threshold

class FilterType(Enum):
    """Used in FilterFactory to identify filter types"""
    NOT_NULL = "not_null"
    GREATER_THAN = "greater_than"
    EQUAL_TO = "equal_to"
    LESS_THAN = "less_than"
    GREATER_THAN_EQUAL_TO = "greater_than_equal_to"
    LESS_THAN_EQUAL_TO = "less_than_equal_to"
    REGEX = "regex"

class FilterFactory:
    """Factory for creating Filter objects from dictionaries"""
    @staticmethod
    def from_dict(f_dict: dict) -> Filter:
        """Create a Filter object from a dictionary"""
        f_type = FilterType(f_dict.get("type"))
        match f_type:
            case FilterType.NOT_NULL:
                return NotNull.from_dict(f_dict)
            case FilterType.REGEX:
                return Regex.from_dict(f_dict)
            case FilterType.GREATER_THAN:
                return GreaterThan.from_dict(f_dict)
            case FilterType.GREATER_THAN_EQUAL_TO:
                return GreaterThanEqualTo.from_dict(f_dict)
            case FilterType.EQUAL_TO:
                return EqualTo.from_dict(f_dict)
            case FilterType.LESS_THAN:
                return LessThan.from_dict(f_dict)
            case FilterType.LESS_THAN_EQUAL_TO:
                return LessThanEqualTo.from_dict(f_dict)
            case _:
                raise ValueError(f"Filter type not supported: {f_type}")