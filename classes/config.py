import json, os, re
from classes.transform import Transform, TransformFactory
from classes.db.interface import DatabaseConnection
from classes.db.config_interface import ConfigDatabaseInterface

class Config:
    def __init__(self, config_name: str, db: DatabaseConnection):
        self.config_interface = ConfigDatabaseInterface(db)

        if os.path.isfile(config_name) and re.match(r".*\.(json|JSON)$", config_name):
            try:
                with open(config_name, "r", encoding="utf-8") as file:
                    self.config = json.load(file)
            except Exception as e:
                raise ValueError(f"Failed to load configuration file: {e}.")
        else:
            read_config = self.config_interface.read_config(config_name)

            if(read_config is None):
                raise ValueError(f"Failed to load config {config_name}. Ensure config profile exists.")

            self.config = json.loads(read_config[0])
        
        self.name = self.config.get("name", "Unnamed Configuration")
        self.description = self.config.get("description", "")
        self.properties = self.config.get("properties", {})
        self.unparsed_transforms = self.config.get("transforms", [])

    def name(self) -> str:
        """Returns the name of the configuration"""
        if isinstance(self.name, str):
            return self.name
        else:
            raise ValueError("Invalid 'name' property in configuration; must be a string.")
    
    def description(self) -> str:
        """Returns the description of the configuration"""
        if isinstance(self.description, str):
            return self.description
        else:
            raise ValueError("Invalid 'description' property in configuration; must be a string.")
    
    def headers(self) -> bool:
        """Returns the headers property"""
        h = self.properties.get("headers", True)

        if isinstance(h, bool):
            return h
        else:
            raise ValueError("Invalid 'headers' property in configuration; must be a boolean.")
        
    def transforms(self) -> list[Transform]:
        """Parses the transforms from the configuration file into a list of parsed tranforms"""
        if isinstance(self.unparsed_transforms, list):
            t = []
            for transform in self.unparsed_transforms:
                t.append(TransformFactory.from_dict(transform))
            return t
        else:
            raise ValueError("Invalid 'transforms' property in configuration; must be a list.")
    
    def __str__(self):
        return f"Config(name={self.name}, description={self.description})"
    
    def __repr__(self):
        return self.__str__()