import os, re, json
import pandas as pd

from .db.interface import DatabaseInterface
from typing import Any
from abc import abstractmethod, ABC


# Make a CSV and config specific reader.
class Reader(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path
        # self.df = pd.read_csv(self.file_path, header=0 if self.headers else None)

    @abstractmethod
    def read(self) -> Any:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

def isFile(file_path: str, pattern: str | None = None) -> bool:
    if pattern is None:
        return os.path.isfile(file_path)
    else:
        return os.path.isfile(file_path) and (re.match(pattern, file_path) is not None)

def isCSV(file_path: str):
    return isFile(file_path, r".*\.(csv|CSV)$")

def isJSON(file_path: str):
    return isFile(file_path, r".*\.(json|JSON)$")

class ConfigReader(Reader):
    def __init__(self, config_name: str, db: DatabaseInterface):
        self.config_name = config_name
        self.db = db
            
    def read(self) -> dict:
        if isJSON(self.config_name):
            try:
                with open(self.config_name, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                raise ValueError(f"Failed to load configuration: {e}")
        else:
            config = self.db.config_read(self.config_name)[0]

            if config is None:
                raise ValueError(f"Failed to load config {self.config_name}")
        
            return json.loads(config)
        
    def __str__(self):
        return f"ConfigReader(config_name={self.config_name})"
            

class DataReader(Reader):
    def __init__(self, file_path: str, headers = True, verbose = False):
        self.headers = headers
        self.verbose = verbose
        self.file_path = file_path

    def read(self) -> pd.DataFrame:

        file_paths = []
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        elif os.path.isdir(self.file_path):
            full_paths = [os.path.join(self.file_path, file) for file in os.listdir(self.file_path)]
            file_paths = [file_path for file_path in full_paths if isCSV(file_path)]
        elif isFile(self.file_path):
            file_paths = [self.file_path]
        else:
            raise ValueError(f"Path is not a file or directory: {self.file_path}")
        
        dfs = [pd.read_csv(file_path, header = 0 if self.headers else None) for file_path in file_paths]
        df = pd.concat(dfs, ignore_index=True)

        return df


    def __str__(self) -> str:
        if os.path.isdir(self.file_path):
            dir_name = os.path.basename(self.file_path)
            dir_path = self.file_path
            return f"CSVReader(dir_name={dir_name}, dir_path={dir_path})"
        elif os.path.isfile(self.file_path):
            file_name = os.path.basename(self.file_path)
            file_path = self.file_path
            return f"CSVReader(file_name={file_name}, file_path={file_path})"
        else:
            raise ValueError(f"CSVReader file_path {self.file_path} is invalid.")