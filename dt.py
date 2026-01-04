#!.dt-venv/bin/python3
from classes.argument_reader import ArgumentReader
from classes.applications.application_factory import ApplicationFactory
from classes.db.interface import DatabaseConnection

def main():
    try:

        db = DatabaseConnection()
        db.init_db()

        arg_reader = ArgumentReader()

        application = ApplicationFactory.create_application(arg_reader, db)

        application.run()
    except Exception as e:
        print(f"Error running dt: {e}")

if __name__ == "__main__":
    main()