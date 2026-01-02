#!.dt-venv/bin/python3
from classes.arg_reader import ArgumentReader
from classes.application import ApplicationFactory
from classes.db import DatabaseInterface

def main():
    try:

        db = DatabaseInterface()
        db.init_db()

        arg_reader = ArgumentReader()

        application = ApplicationFactory.create_application(arg_reader, db)

        application.run()

    except Exception as e:
        print(f"Error running dt: {e}")
        return
    
    return

if __name__ == "__main__":
    main()