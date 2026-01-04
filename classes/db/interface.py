import sqlite3

class DatabaseConnection:
    def __init__(self):
        self.con = sqlite3.connect("db.sqlite")

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
            cents INTEGER,
            amount REAL GENERATED ALWAYS AS (cents / 100) VIRTUAL)
            """
        )
        self.con.commit()

class DatabaseInterface:
    def __init__(self, database_connection: DatabaseConnection):
        self.connection = database_connection.con