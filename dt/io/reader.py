import os
import pandas as pd

class ReaderFactory:
    @staticmethod
    def create_readers(file_paths: list[str], headers = True, verbose=False):
        return [ReaderFactory.create_reader(file_path, headers, verbose) for file_path in file_paths]

    @staticmethod
    def create_reader(file_path: str, headers = True, verbose=False):
        return Reader(file_path, headers, verbose)

# Make a CSV and config specific reader.
class Reader:
    def __init__(self, file_path: str, headers = True, verbose = False):
        self.file_path = file_path
        self.headers = headers
        self.verbose = verbose
        self.df = pd.read_csv(self.file_path, header=0 if self.headers else None)

    def read(self):
        if self.verbose:
            print(self)
        
        return self.df

    def __str__(self):
        file_name = os.path.basename(self.file_path)
        return f"Reader({file_name})(file_path={self.file_path}, columns={self.df.columns.values}, rows={len(self.df)})"