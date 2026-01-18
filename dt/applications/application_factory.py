from dt.helpers.argument_reader import ArgumentReader
from dt.db.interface import DatabaseConnection
from .application import Application
from .config_application import ConfigApplication
from .transform_application import TransformApplication

class ApplicationFactory:
    @staticmethod
    def create_application(argument_reader: ArgumentReader, db: DatabaseConnection) -> Application:
        match(argument_reader.get_application()):
            case "transform":
                return TransformApplication(argument_reader.args, db)
            case "config":
                return ConfigApplication(argument_reader.args, db)
        
        raise Exception()