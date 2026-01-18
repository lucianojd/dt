#!.dt-venv/bin/python3
import sys
from dt.helpers.argument_reader import ArgumentReader
from dt.applications.application_factory import ApplicationFactory
from dt.db.interface import DatabaseConnection

def main():
    try:
        # Create database instance.
        db = DatabaseConnection(sys.argv[0])
        db.init_db()

        # Create parser.
        arg_reader = ArgumentReader()

        # Attach applications.

        # Determine application to run.
        application = ApplicationFactory.create_application(arg_reader, db)

        application.run()
    except Exception as e:
        print(f"Error running dt: {e}")

if __name__ == "__main__":
    main()