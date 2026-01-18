import os, argparse, re

from .application import Application
from dt.db.interface import DatabaseConnection
from dt.helpers.config import Config
from dt.io.reader import Reader, ReaderFactory
from dt.helpers.transform import Transformer
from dt.io.writer import Writer

class TransformApplication(Application):
    def __init__(self, args: argparse.Namespace, db: DatabaseConnection):
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

            writer = Writer(self.db, self.output, self.verbose, self.append)
        
            # Want to adjust this logic so the reader creates one large data frame instead of multiple dataframes.
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