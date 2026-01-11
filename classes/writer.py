import pandas as pd
from classes.db.writer_interface import WriterDatabaseInterface
from classes.db.interface import DatabaseConnection

class Writer:
    """Class for writing the data to a file. Currently supports CSV format only."""
    def __init__(self, db: DatabaseConnection, file_path: str | None, verbose=False, append=False):
        self.db = db
        self.file_path = file_path
        self.verbose = verbose
        self.append = append
        self.data = pd.DataFrame()

    def add_entry(self, df: pd.DataFrame):
        """Add a single data frame to the writer's data frame."""
        if df.empty is False:
            if self.data.empty is True:
                self.data = df.copy()
            else:
                self.data = pd.concat([self.data, df], ignore_index=True)

    def add_entries(self, dfs: list[pd.DataFrame]):
        """Add multiple data frames to the writer's data frame."""
        entries = [df for df in dfs if df.empty is False]
        if self.data.empty is True:
            self.data = pd.concat(entries, ignore_index=True)
        else:
            self.data = pd.concat([self.data] + entries, ignore_index=True)
    
    def write(self):
        """Write the data frame to the output file in CSV format."""
        if isinstance(self.file_path, str):
            self.data.to_csv(
                self.file_path, 
                index=False, 
                float_format="%.2f", 
                date_format="%Y-%m-%d", 
                header=self.append is False, 
                mode="a" if self.append is True else "w"
            )
        else:
            writer_interface = WriterDatabaseInterface(self.db)
            writer_interface.transactions_insert(self.data)