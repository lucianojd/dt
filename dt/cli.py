#!.dt-venv/bin/python3
import sys
from dt.io.argument_parser import ArgumentReader
from dt.lib.application import ApplicationFactory
from dt.io.db.interface import DatabaseInterface
from dt.lib.application import ConfigApplication, TransformApplication

def main():
    try:
        database_interface = DatabaseInterface(sys.argv[0])
        
        # Create parser.
        arg_reader = ArgumentReader()

        # Attach applications.
        ConfigApplication.attach(arg_reader.get_subparser())
        TransformApplication.attach(arg_reader.get_subparser())

        # Determine application to run.
        application = ApplicationFactory.create_application(arg_reader, database_interface)
        application.run()

    except Exception as e:
        print(f"Error running dt: {e}")

if __name__ == "__main__":
    main()