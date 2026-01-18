import pandas as pd
from enum import Enum

class Assignment:
    def __init__(self, column: str | int, value: str | int | float):
        self.name = ""
        self.column = column
        self.value = value

    def assign(self, df: pd.DataFrame, filter: pd.Series | None = None) -> None:
        """Apply the assignment to the DataFrame data which meets the filter condition."""
        if filter is None:
            df[self.column] = self.value
        else:
            df.loc[filter, self.column] = self.value

    def __str__(self) -> str:
        return f"{self.name}(column={self.column}, value={self.value})"
    
    def __repr__(self) -> str:
        return self.__str__()

class ColumnAssignment(Assignment):
    """Assign the value of one column to another column."""
    def __init__(self, column, value):
        self.name = "ColumnAssignment"
        super().__init__(column, value)

    def assign(self, df: pd.DataFrame, filter: pd.Series | None = None) -> None:
        if filter is None:
            df[self.column] = df[self.value]
        else:
            df.loc[filter, self.column] = df[self.value]

class IntAssignment(Assignment):
    """Assign an integer value to a column."""
    def __init__(self, column, value):
        self.name = "IntAssignment"
        super().__init__(column, int(value))
    
class StringAssignment(Assignment):
    """Assign a string value to a column."""
    def __init__(self, column, value):
        self.name = "StringAssignment"
        super().__init__(column, str(value))

class FloatAssignment(Assignment):
    """Assign a float value to a column."""
    def __init__(self, column, value):
        self.name = "FloatAssignment"
        super().__init__(column, float(value))

class AssignmentType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    COLUMN = "column"

class AssignmentFactory:
    @staticmethod
    def create_assignment(type: AssignmentType, column: str | int, value: str | int | float) -> Assignment:
        """
        Create an assignment object based on the assignment type.
        When assignment type is COLUMN the value is the source column name or index.
        """
        match type:
            case AssignmentType.STRING:
                return StringAssignment(column, value)
            case AssignmentType.INTEGER:
                return IntAssignment(column, value)
            case AssignmentType.FLOAT:
                return FloatAssignment(column, value)
            case AssignmentType.COLUMN:
                return ColumnAssignment(column, value)
            case _:
                raise ValueError(f"Assignment type not supported: {type}")

    @staticmethod
    def from_dict(a_dict: dict) -> Assignment:
        """
        Create an assignment object from a dictionary.
        """
        a_type = AssignmentType(a_dict.get("type"))
        column = a_dict.get("column")
        value = a_dict.get("value")

        if column is None or value is None:
            raise ValueError("Assignment dictionary must contain 'column' and 'value' keys.")
        
        if isinstance(column, (int, str)) and isinstance(value, (int, float, str)):
            return AssignmentFactory.create_assignment(a_type, column, value)
        else:
            raise ValueError("Invalid types for 'column' or 'value' in assignment dictionary.")
        