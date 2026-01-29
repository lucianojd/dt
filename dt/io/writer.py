import pandas as pd
from dt.io.db.interface import DatabaseInterface

class Writer:
    """Class for writing the data to a file. Currently supports CSV format only."""
    def __init__(self, db: DatabaseInterface, file_path: str | None, verbose=False, append=False):
        self.db = db
        self.file_path = file_path
        self.verbose = verbose
        self.append = append
    
    def write(self, df: pd.DataFrame):
        """Write the data frame to the output file in CSV format."""
        if isinstance(self.file_path, str):
            df.to_csv(
                self.file_path, 
                index=False, 
                float_format="%.2f", 
                date_format="%Y-%m-%d", 
                header=self.append is False, 
                mode="a" if self.append is True else "w"
            )
        else:
            self.db.transactions_insert(df)