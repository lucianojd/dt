# Create application manager for handling which application is determined to run.
# Adjust applications so that arguments are passed after the application is created.

from os import path
from pathlib import Path
from argparse import Namespace
from abc import abstractmethod, ABC
from dt.io.db.interface import DatabaseInterface
from dt.lib.config import Config
from dt.io.reader import DataReader
from dt.lib.transform import Transformer
from dt.io.argument_parser import ArgumentReader
from argparse import ArgumentParser, _SubParsersAction
from dt.lib.transaction import TransactionList

class Application(ABC):
    @staticmethod
    @abstractmethod
    def attach(subparser: _SubParsersAction[ArgumentParser]):
        raise RuntimeError(f"attach method was not implemented for \"self.application\" application")

    @abstractmethod
    def run(self) -> None:
        raise RuntimeError(f"run method was not implemanted for \"{self.__class__.__name__}\" application")

class ConfigApplication(Application):
    def __init__(self, args: Namespace, db: DatabaseInterface):
        self.db = db
        self.database_inteface = db
        self.args = args

    @staticmethod
    def attach(subparser: _SubParsersAction[ArgumentParser]):
        config_parser = subparser.add_parser("config")
        config_modes = config_parser.add_subparsers(dest="mode", help="Config applications")

        config_modes_add = config_modes.add_parser("add")
        config_modes_add.add_argument('file', type=str, help="Location of the config file")

        config_modes.add_parser("list")

        config_modes_delete = config_modes.add_parser("delete")
        config_modes_delete.add_argument('name', type=str, help="Name of the configuration to be deleted")

        config_modes_info = config_modes.add_parser("info")
        config_modes_info.add_argument('name', type=str, help="Print details about the configuration")
    
    def run(self) -> None:
        match(self.args.mode):
            case "add":
                name = path.basename(Path(self.args.file).stem)
                
                with open(self.args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.database_inteface.config_insert(name, content)
            case "list":
                configs = self.database_inteface.config_list()
                print(f"Saved profiles ({len(configs)})\n-----")
                for index, config in enumerate(configs):
                    print(f"{index+1}| {config[0]}")
            case "delete":
                self.database_inteface.config_delete(self.args.name)
            case "info":
                config = Config(self.args.name, self.db)
                print(config)
            case _:
                raise Exception(f"Unknown config application mode: \"{self.args.mode}\"")


class TransformApplication(Application):
    def __init__(self, args: Namespace, db: DatabaseInterface):
        self.db = db

        try:
            self.config = Config(args.config, db)
            
            self.paths = args.paths
            self.verbose = args.verbose
            self.output = args.output
            self.append = args.append
        except Exception as e:
            print(f"Error creating \"{self.__class__.__name__}\": {e}")

    @staticmethod
    def attach(subparser: _SubParsersAction[ArgumentParser]):
        transform_parser = subparser.add_parser("transform", description="Application performs data transformations based on the specified configuration")
        transform_parser.add_argument("-c", "--config", required=True, type=str, help="path to the configuration file")
        transform_parser.add_argument("paths", nargs="+", type=str, help="the path to the bank statement file")
        transform_parser.add_argument("-a", "--append", action="store_true", help="append to the output file instead of overwriting")
        transform_parser.add_argument("-o", "--output", type=str, help="the path to the output file (default: output.csv)")

    def run(self) -> None:
        # Need to handle the list that is currently coming in.
        reader = DataReader(self.paths, headers=self.config.headers(), verbose=self.verbose)
        try:
            df = reader.read()
        except Exception as e:
            print(f"Error reading files:\n {reader}: {e}")
            return
        
        try:
            transformer = Transformer(self.verbose)
            transformer.set_transforms(self.config.transforms())
            df = transformer.transform(df)
        except Exception as e:
            print(f"Error transforming data from file {reader}: {e}")
            return
        
        try:
            transaction_list = TransactionList.from_dataframe(df)

            if self.output is None:
                transaction_list.write_to_db(self.db, verbose=self.verbose)
            else:
                transaction_list.write_to_csv(self.output, self.append, self.verbose)
        except Exception as e:
            print(f"Error creating transaction list from data frame: {e}")
            return

    def __str__(self) -> str:
        return f"paths=({self.paths})"

class ApplicationFactory:
    @staticmethod
    def create_application(argument_reader: ArgumentReader, db: DatabaseInterface) -> Application:
        match(argument_reader.get_application()):
            case "transform":
                return TransformApplication(argument_reader.get_args(), db)
            case "config":
                return ConfigApplication(argument_reader.get_args(), db)
        
        raise Exception(f"Unable to create application: \"{argument_reader.get_application}\"")