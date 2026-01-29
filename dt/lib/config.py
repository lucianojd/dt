from dt.lib.transform import Transform, TransformFactory
from dt.io.db.interface import DatabaseInterface
from dt.io.reader import ConfigReader

class Config:
    def __init__(self, config_name: str, db: DatabaseInterface):
        config_reader = ConfigReader(config_name, db)
        config_data = config_reader.read()
        
        self.name = config_data.get("name", "Unnamed Configuration")
        self.description = config_data.get("description", "")
        self.properties = config_data.get("properties", {})
        self.unparsed_transforms = config_data.get("transforms", [])

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