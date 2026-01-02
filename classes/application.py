import argparse, os, re, pathlib
from classes.config import Config
from classes.arg_reader import ArgumentReader
from classes.reader import ReaderFactory
from classes.writer import Writer
from classes.transform import Transformer
from classes.db import DatabaseInterface

class Application:
    def __init__(self, application: str):
        self.application = application

    def run(self) -> None:
        raise RuntimeError(f"run method was not implemanted for \"{self.application}\" application")

class ConfigApplication(Application):
    def __init__(self, args: argparse.Namespace, db: DatabaseInterface):
        super().__init__("config")
        self.db = db
        self.mode = args.mode
        self.args = args

    def run(self) -> None:
        match(self.mode):
            case "add":
                name = os.path.basename(pathlib.Path(self.args.file).stem)
                
                with open(self.args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.db.config_insert(name, content)
            case "list":
                configs = self.db.config_list()
                print(f"Saved profiles ({len(configs)})\n-----")
                for index, config in enumerate(configs):
                    print(f"{index+1}| {config[0]}")
            case "delete":
                self.db.config_delete(self.args.name)


class TransformApplication(Application):
    def __init__(self, args: argparse.Namespace, db: DatabaseInterface):
        super().__init__("transform")
        self.db = db

        try:
            self.config = Config(args.config, db)
            self.paths = self._get_paths(args)

            self.verbose = args.verbose
            self.output = args.output
            self.append = args.append
        except Exception as e:
            print(f"Error creating \"{self.application}\": {e}")

    def run(self) -> None:
        try:
            readers = ReaderFactory.create_readers(self.paths, headers=self.config.headers(), verbose=self.verbose)

            transformer = Transformer(self.verbose)
            transformer.set_transforms(self.config.transforms())

            writer = Writer(self.output,verbose=self.verbose,append=self.append)
        
            for reader in readers:
                try: 
                    df = reader.read()
                except Exception as e:
                    print(f"Error reading file {reader.file_path}: {e}")
                    return
                
                try: 
                    df = transformer.transform(df)
                except Exception as e:
                    print(f"Error transforming data from file {reader.file_path}: {e}")
                    return
                    
                try:
                    writer.add_entry(df)
                except Exception as e:
                    print(f"Error adding data from file {reader.file_path} to writer: {e}")
                    return
                
            try:
                writer.write()
            except Exception as e:
                print(f"Error writing output file {writer.file_path}: {e}")
                return
            
        except Exception as e:
            print(f"Error creating readers: {e}")
            return

    def _get_paths(self, args: argparse.Namespace):
        """Get a list of valid file paths from the provided arguments."""
        file_paths = []

        for path in args.paths:
            if os.path.exists(path) is False:
                raise FileNotFoundError(f"File not found: {path}")
            elif os.path.isdir(path) is True:
                for file in os.listdir(path):
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path) is True and re.match(r".*\.(csv|CSV)$", file):
                        file_paths.append(full_path)
            elif os.path.isfile(path) is True:
                file_paths.append(path)
            else:
                raise ValueError(f"Path is not a file or directory: {path}")

        return file_paths

    def __str__(self) -> str:
        return f"paths=({self.paths})"

class ApplicationFactory:
    @staticmethod
    def create_application(argument_reader: ArgumentReader, db: DatabaseInterface) -> Application:
        match(argument_reader.get_application()):
            case "transform":
                return TransformApplication(argument_reader.args, db)
            case "config":
                return ConfigApplication(argument_reader.args, db)
        
        raise Exception()