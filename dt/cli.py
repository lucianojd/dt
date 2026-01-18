#!.dt-venv/bin/python3
import sys
from dt.helpers.argument_reader import ArgumentReader
from dt.applications.application_factory import ApplicationFactory
from dt.db.interface import DatabaseConnection

def main():
    try:
        db = DatabaseConnection(sys.argv[0])
        db.init_db()

        arg_reader = ArgumentReader()

        application = ApplicationFactory.create_application(arg_reader, db)

        application.run()
    except Exception as e:
        print(f"Error running dt: {e}")

if __name__ == "__main__":
    main()