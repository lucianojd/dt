import sqlite3
import pathlib

from pandas import DataFrame
from hashlib import sha256

class DatabaseInitializer:
    def __init__(self, executable_path: str):
        parent_folder = pathlib.Path(executable_path).parent
        self.connection = sqlite3.connect(f"{parent_folder}/db.sqlite")

    def init_db(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            config TEXT NOT NULL)
            """
        )

        self.connection.execute(
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
        
        self.connection.commit()

class DatabaseInterface:
    def __init__(self, executable_path: str):
        initializer = DatabaseInitializer(executable_path)
        initializer.init_db()

        self.connection = initializer.connection

    def config_insert(self, name, config):
        try:
            self.connection.execute(
                """
                INSERT INTO configs (name, config) VALUES (?, ?)
                """,
                (name, config)
            )
            self.connection.commit()
        except Exception as e:
            print(e)

    def config_list(self):
        cursor = self.connection.cursor()
        rows = cursor.execute("SELECT name FROM configs").fetchall()
        cursor.close()

        return rows
    
    def config_delete(self, name):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM configs WHERE name = ?", (name,))
        self.connection.commit()
        cursor.close()

    def config_read(self, name):
        cursor = self.connection.cursor()
        query = cursor.execute("SELECT config FROM configs WHERE name = ?", (name,))
        config = query.fetchone()
        cursor.close()
        return config

    def transactions_fetch_all(self):
        cursor = self.connection.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        return rows

    def transactions_count(self):
        cursor = self.connection.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]
        return count
    

    def transactions_insert(self, transactions: DataFrame):
        try:
            transactions["id"] = transactions.apply(lambda row: sha256("".join(str(value) for value in row).encode()).hexdigest(), axis=1)
            transactions.drop_duplicates(subset=["id"], inplace=True)
            transactions.to_sql("transactions", self.connection, if_exists="append", index=False)
        except Exception as e:
            print(type(e).__name__)

            raise Exception(f"Error inserting transactions into database: {e}")