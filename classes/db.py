import sqlite3

class DatabaseConnection:
    def __init__(self):
        self.con = sqlite3.connect("db.sqlite")

class DatabaseInterface:
    def __init__(self):
        self.database_connection = DatabaseConnection()
        self.con = self.database_connection.con

    def init_db(self):
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            config TEXT NOT NULL)
            """
        )
        self.con.commit()
    
    def config_insert(self, name, config):
        try:
            self.con.execute(
                """
                INSERT INTO configs (name, config) VALUES (?, ?)
                """,
                (name, config)
            )
            self.con.commit()
        except Exception as e:
            print(e)

    def config_list(self):
        cursor = self.con.cursor()
        rows = cursor.execute("SELECT name FROM configs").fetchall()
        cursor.close()

        return rows
    
    def config_delete(self, name):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM configs WHERE name = ?", (name,))
        self.con.commit()
        cursor.close()

    def read_config(self, name):
        cursor = self.con.cursor()
        query = cursor.execute("SELECT config FROM configs WHERE name = ?", (name,))
        config = query.fetchone()
        cursor.close()
        return config