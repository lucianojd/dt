import argparse, os, pathlib
from .application import Application
from dt.db.interface import DatabaseConnection
from dt.db.config_interface import ConfigDatabaseInterface
from dt.helpers.config import Config

class ConfigApplication(Application):
    def __init__(self, args: argparse.Namespace, db: DatabaseConnection):
        super().__init__("config")
        self.db = db
        self.database_inteface = ConfigDatabaseInterface(db)
        self.mode = args.mode
        self.args = args

    def run(self) -> None:
        match(self.mode):
            case "add":
                name = os.path.basename(pathlib.Path(self.args.file).stem)
                
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

                print(f"Name:\n\t{config.name}")
                print(f"Description:\n\t{config.description}")
                print(f"Headers:\n\t{config.headers()}")

                print("Transforms:")
                transforms = config.transforms()
                for transform in transforms:
                    print(f"\t{transform}")
