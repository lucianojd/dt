import os, re, json
import pandas as pd

from .db.interface import DatabaseInterface
from typing import Any
from abc import abstractmethod, ABC


# Make a CSV and config specific reader.
class Reader(ABC):
    @abstractmethod
    def read(self) -> Any:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

def isDir(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)

def isFile(file: str, pattern: str | None = None) -> bool:
    if pattern is None:
        return os.path.exists(file) and os.path.isfile(file)
    else:
        return os.path.exists(file) and os.path.isfile(file) and (re.match(pattern, file) is not None)

def isCSV(file: str):
    return isFile(file, r".*\.(csv|CSV)$")

def isJSON(file: str):
    return isFile(file, r".*\.(json|JSON)$")

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
    def __init__(self, file_paths: list[str], headers = True, verbose = False):
        self.headers = headers
        self.verbose = verbose
        self.file_paths = file_paths

    def read(self) -> pd.DataFrame:
        file_paths = []
        for file_path in self.file_paths:
            if isDir(file_path):
                files = [os.path.join(file_path, file) for file in os.listdir(file_path)]
                file_paths += ([file for file in files if isCSV(file)])
            elif isFile(file_path):
                file_paths.append(file_path)
            else:
                raise ValueError(f"Path is not a file or directory: {file_path}")
        
        dfs = [pd.read_csv(file_path, header = 0 if self.headers else None) for file_path in file_paths]
        dfs = [df for df in dfs if not df.empty]
        df = pd.concat(dfs, ignore_index=True)

        return df


    def __str__(self) -> str:
        output = ""
        for index, path in enumerate(self.file_paths):
            if os.path.isdir(path):
                dir_name = os.path.basename(path)
                output += f"CSVReader(dir_name={dir_name}, dir_path={path})"
            elif os.path.isfile(path):
                file_name = os.path.basename(path)
                output += f"CSVReader(file_name={file_name}, file_path={path})"
            else:
                raise ValueError(f"CSVReader file_path {path} is invalid.")

            if index < len(self.file_paths) - 1:
                output += "\n"

        return output