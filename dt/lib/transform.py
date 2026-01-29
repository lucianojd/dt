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
    def __init__(self, type: TransformType):
        self.type = type

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the transform to the given data frame and return the transformed data frame."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

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
        super().__init__(TransformType.CONDITIONAL_UPDATE)
        self.filter = filter
        self.assignments = assignments

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if len(self.filter) == 0:
            condition = pd.Series([True] * len(df))
        else:
            condition = reduce(operator.and_, (f.apply(df) for f in self.filter))

        for assignment in self.assignments:
            assignment.assign(df, condition)

        return df

    def __str__(self) -> str:
        return f"ConditionalUpdate(filter={self.filter}, assignments={self.assignments})"

class TrimStrings(Transform):
    def __init__(self, columns: list[str | int]):
        super().__init__(TransformType.TRIM_STRINGS)
        self.columns = columns

    def transform(self, df: pd.DataFrame):
        for col in self.columns:
            df[col] = df[col].transform(lambda s: s.strip() if isinstance(s, str) else s)
        
        return df

    def __str__(self) -> str:
        return f"TrimStrings(columns={self.columns})"

class ReadDate(Transform):
    def __init__(self, columns: list[str | int], date_format: str):
        super().__init__(TransformType.DATE)
        self.columns = columns
        self.date_format = date_format

    def transform(self, df):
        for col in self.columns:
            df[col] = df[col].transform(lambda date: dt.strptime(date, self.date_format))
        return df

    def __str__(self) -> str:
        return f"DateTransform(columns={self.columns}, date_format={self.date_format})"


class RenameColumns(Transform):
    def __init__(self, columns: dict[str | int , str | int]):
        super().__init__(TransformType.RENAME_COLUMNS)
        self.columns = columns

    def transform(self, df: pd.DataFrame):
        return df.rename(columns=self.columns)
    
    def __str__(self) -> str:
        return f"RenameColumns(columns={self.columns})"
    
class CreateColumn(Transform):
    def __init__(self, column: int | str, default: int | str | float):
        super().__init__(TransformType.CREATE_COLUMN)
        self.column = column
        self.default = default

    def transform(self, df: pd.DataFrame):
        df[self.column] = self.default
        return df
    
    def __str__(self):
        return f"CreateColumn(column={self.column}, default_value={self.default})"
    
class DropColumns(Transform):
    def __init__(self, columns: list[int | str]):
        super().__init__(TransformType.DROP_COLUMNS)
        self.columns = columns

    def transform(self, df: pd.DataFrame):
        return df.drop(self.columns, axis=1)

    def __str__(self):
        return f"DropColumns(columns={self.columns})"
    
class ReorderColumns(Transform):
    def __init__(self, columns: list[int | str]):
        super().__init__(TransformType.REORDER_COLUMNS)
        self.columns = columns

    def transform(self, df: pd.DataFrame):
        return df.reindex(columns=self.columns)

    def __str__(self):
        return f"ReorderColumns(columns={self.columns})"
    
class AbsoluteValue(Transform):
    def __init__(self, columns: list[int | float]):
        super().__init__(TransformType.ABSOLUTE_VALUE)
        self.columns = columns

    def transform(self, df: pd.DataFrame):
        for col in self.columns:
            df[col] = abs(df[col])
        return df

    def __str__(self):
        return f"AbsoluteValue(columns={self.columns})"

class TransformFactory:
    @staticmethod
    def from_dict(t_dict: dict) -> Transform:
        t_type = TransformType(t_dict.get("type"))

        if t_type == TransformType.RENAME_COLUMNS:
            columns = t_dict.get("columns")
            if isinstance(columns, dict):
                return RenameColumns(columns)
            elif isinstance(columns, list):
                return RenameColumns({index : name for index, name in enumerate(columns)})
            else:
                raise ValueError("Invalid 'columns' property for RenameColumns; must be a dict or list.")
        elif t_type == TransformType.CREATE_COLUMN:
            name = t_dict.get("name")
            default_value = t_dict.get("default_value")

            if isinstance(name, (str | int)) and isinstance(default_value, (str | int | float)):
                return CreateColumn(name, default_value)
            else:
                raise ValueError("Invalid 'name' or 'default_value' property for CreateColumn; must be str|int and str|int|float respectively.")
        elif t_type == TransformType.CONDITIONAL_UPDATE:
            filters = [FilterFactory.from_dict(f) for f in t_dict.get("filters", [])]
            assignments = [AssignmentFactory.from_dict(a) for a in t_dict.get("assignments", [])]
            return ConditionalUpdate(filters, assignments)
        elif t_type == TransformType.ABSOLUTE_VALUE:
            return AbsoluteValue(t_dict.get("columns", []))
        elif t_type == TransformType.DATE:
            return ReadDate(t_dict.get("columns", []), t_dict.get("date_format", ""))
        elif t_type == TransformType.DROP_COLUMNS:
            return DropColumns(t_dict.get("columns", []))
        elif t_type == TransformType.REORDER_COLUMNS:
            return ReorderColumns(t_dict.get("columns", []))
        elif t_type == TransformType.TRIM_STRINGS:
            return TrimStrings(t_dict.get("columns", []))
        else:
            raise ValueError(f"Unknown transform type: {t_type}")