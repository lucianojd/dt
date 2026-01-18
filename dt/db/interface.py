import sqlite3
import pathlib

class DatabaseConnection:
    def __init__(self, executable_path: str):
        parent_folder = pathlib.Path(executable_path).parent
        self.con = sqlite3.connect(f"{parent_folder}/db.sqlite")

    def init_db(self):
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            config TEXT NOT NULL)
            """
        )

        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            date TEXT,
            description TEXT,
            institution TEXT,
            type TEXT,
            amount REAL)
            """
        )
        
        self.con.commit()

class DatabaseInterface:
    def __init__(self, database_connection: DatabaseConnection):
        self.connection = database_connection.con