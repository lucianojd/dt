import pandas as pd
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime as dt
from .filter import Filter, FilterFactory
from .assignment import Assignment, AssignmentFactory
from functools import reduce
import operator

class TransformType(Enum):
    READ_DATE = "read_date"
    RENAME_COLUMNS = "rename_columns"
    DROP_COLUMNS = "drop_columns"
    REORDER_COLUMNS = "reorder_columns"
    CREATE_COLUMN = "create_column"
    CONDITIONAL_UPDATE = "conditional_update"
    DATE = "date"
    TRIM_STRINGS = "trim_strings"
    ABSOLUTE_VALUE = "absolute_value"

class Transform(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the transform to the given data frame and return the transformed data frame."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return self.__str__()

class Transformer:
    def __init__(self, verbose = False):
        self.transforms: list[Transform] = []
        self.verbose = verbose

    def add_transform(self, transform: Transform):
        """Add a transform to the list of transforms."""
        self.transforms.append(transform)

    def set_transforms(self, transforms: list[Transform]):
        """Set the list of transforms."""
        self.transforms = transforms

    # Change this to return a list of transaction objects.
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all transforms to the given data frame and return the transformed data frame."""
        for t in self.transforms:
            if self.verbose:
                print(t)
            df = t.transform(df)
        return df

class ConditionalUpdate(Transform):
    def __init__(self, filter: list[Filter], assignments: list[Assignment]):
        self.filter = filter
        self.assignments = assignments

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        filters = [FilterFactory.from_dict(f) for f in t_dict.get("filters", [])]
        assignments = [AssignmentFactory.from_dict(a) for a in t_dict.get("assignments", [])]
        return cls(filters, assignments)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if len(self.filter) == 0:
            condition = pd.Series([True] * len(df))
        else:
            condition = reduce(operator.and_, (f.apply(df) for f in self.filter))

        for assignment in self.assignments:
            assignment.assign(df, condition)

        return df

    def __str__(self) -> str:
        return f"{super().__str__()}(filter={self.filter}, assignments={self.assignments})"

class TrimStrings(Transform):
    def __init__(self, columns: list[str | int]):
        self.columns = columns

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        columns = t_dict.get("columns")
        if isinstance(columns, list):
            return cls(columns)
        else:
            raise ValueError("Invalid 'columns' property for TrimStrings; must be a list.")

    def transform(self, df: pd.DataFrame):
        for col in self.columns:
            df[col] = df[col].transform(lambda s: s.strip() if isinstance(s, str) else s)
        
        return df

    def __str__(self) -> str:
        return f"{super().__str__()}(columns={self.columns})"

class ReadDate(Transform):
    def __init__(self, columns: list[str | int], date_format: str):
        self.columns = columns
        self.date_format = date_format

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        columns = t_dict.get("columns")
        date_format = t_dict.get("date_format")
        if isinstance(columns, list) and isinstance(date_format, str):
            return cls(columns, date_format)
        else:
            raise ValueError("Invalid 'columns' or 'date_format' property for ReadDate; must be a list and a string respectively.")

    def transform(self, df):
        for col in self.columns:
            df[col] = df[col].transform(lambda date: dt.strptime(date, self.date_format))
        return df

    def __str__(self) -> str:
        return f"{super().__str__()}(columns={self.columns}, date_format={self.date_format})"


class RenameColumns(Transform):
    def __init__(self, columns: dict[str | int , str | int]):
        self.columns = columns

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        columns = t_dict.get("columns")
        if isinstance(columns, dict):
            return cls(columns)
        elif isinstance(columns, list):
            return cls({index : name for index, name in enumerate(columns)})
        else:
            raise ValueError("Invalid 'columns' property for RenameColumns; must be a dict or list.")

    def transform(self, df: pd.DataFrame):
        return df.rename(columns=self.columns)
    
    def __str__(self) -> str:
        return f"{super().__str__()}(columns={self.columns})"
    
class CreateColumn(Transform):
    def __init__(self, column: int | str, default: int | str | float):
        self.column = column
        self.default = default

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        name = t_dict.get("name")
        default_value = t_dict.get("default_value")

        if isinstance(name, (str | int)) and isinstance(default_value, (str | int | float)):
            return cls(name, default_value)
        else:
            raise ValueError("Invalid 'name' or 'default_value' property for CreateColumn; must be str|int and str|int|float respectively.")

    def transform(self, df: pd.DataFrame):
        df[self.column] = self.default
        return df
    
    def __str__(self):
        return f"{super().__str__()}(column={self.column}, default_value={self.default})"
    
class DropColumns(Transform):
    def __init__(self, columns: list[int | str]):
        self.columns = columns

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        columns = t_dict.get("columns")
        if isinstance(columns, list):
            return cls(columns)
        else:
            raise ValueError("Invalid 'columns' property for DropColumns; must be a list.")

    def transform(self, df: pd.DataFrame):
        return df.drop(self.columns, axis=1)

    def __str__(self):
        return f"{super().__str__()}(columns={self.columns})"
    
class ReorderColumns(Transform):
    def __init__(self, columns: list[int | str]):
        self.columns = columns

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        columns = t_dict.get("columns")
        if isinstance(columns, list):
            return cls(columns)
        else:
            raise ValueError("Invalid 'columns' property for ReorderColumns; must be a list.")

    def transform(self, df: pd.DataFrame):
        return df.reindex(columns=self.columns)

    def __str__(self):
        return f"{super().__str__()}(columns={self.columns})"
    
class AbsoluteValue(Transform):
    def __init__(self, columns: list[int | float]):
        self.columns = columns

    @classmethod
    def from_dict(cls, t_dict: dict) -> Transform:
        columns = t_dict.get("columns")
        if isinstance(columns, list):
            return cls(columns)
        else:
            raise ValueError("Invalid 'columns' property for AbsoluteValue; must be a list.")

    def transform(self, df: pd.DataFrame):
        for col in self.columns:
            df[col] = abs(df[col])
        return df

    def __str__(self):
        return f"{super().__str__()}(columns={self.columns})"

class TransformFactory:
    @staticmethod
    def from_dict(t_dict: dict) -> Transform:
        t_type = TransformType(t_dict.get("type"))

        match t_type:
            case TransformType.RENAME_COLUMNS:
                return RenameColumns.from_dict(t_dict)
            case TransformType.CREATE_COLUMN:
                return CreateColumn.from_dict(t_dict)
            case TransformType.CONDITIONAL_UPDATE:
                return ConditionalUpdate.from_dict(t_dict)
            case TransformType.ABSOLUTE_VALUE:
                return AbsoluteValue.from_dict(t_dict)
            case TransformType.DATE:
                return ReadDate.from_dict(t_dict)
            case TransformType.DROP_COLUMNS:
                return DropColumns.from_dict(t_dict)
            case TransformType.REORDER_COLUMNS:
                return ReorderColumns.from_dict(t_dict)
            case TransformType.TRIM_STRINGS:
                return TrimStrings.from_dict(t_dict)
            case _:
                raise ValueError(f"Unknown transform type: {t_type}")