import json
from classes.transform import Transform, TransformFactory

class Config:
    def __init__(self, config_path: str):
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                self.config = json.load(file)

                self.name = self.config.get("name", "Unnamed Configuration")
                self.description = self.config.get("description", "")
                self.properties = self.config.get("properties", {})
                self.unparsed_transforms = self.config.get("transforms", [])

        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {e}")
        
    def name(self) -> str:
        if isinstance(self.name, str):
            return self.name
        else:
            raise ValueError("Invalid 'name' property in configuration; must be a string.")
    
    def description(self) -> str:
        if isinstance(self.description, str):
            return self.description
        else:
            raise ValueError("Invalid 'description' property in configuration; must be a string.")
    
    def headers(self) -> bool:
        h = self.properties.get("headers", True)

        if isinstance(h, bool):
            return h
        else:
            raise ValueError("Invalid 'headers' property in configuration; must be a boolean.")
        
    def transforms(self) -> list[Transform]:
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