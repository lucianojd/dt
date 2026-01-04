from .interface import DatabaseConnection, DatabaseInterface

class ConfigDatabaseInterface(DatabaseInterface):
    def __init__(self, database_connnection: DatabaseConnection) -> None:
        super().__init__(database_connnection)

    
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

    def read_config(self, name):
        cursor = self.connection.cursor()
        query = cursor.execute("SELECT config FROM configs WHERE name = ?", (name,))
        config = query.fetchone()
        cursor.close()
        return config