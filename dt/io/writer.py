import pandas as pd
from dt.io.db.interface import DatabaseInterface

class Writer:
    """Class for writing the data to a file. Currently supports CSV format only."""
    def __init__(self, db: DatabaseInterface, file_path: str | None, verbose=False, append=False):
        self.db = db
        self.file_path = file_path
        self.verbose = verbose
        self.append = append
