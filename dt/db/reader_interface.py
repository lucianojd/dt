from .interface import DatabaseConnection, DatabaseInterface

class ReaderDatabaseInterface(DatabaseInterface):
    def __init__(self, database_connection: DatabaseConnection) -> None:
        super().__init__(database_connection)

    def transactions_fetch_all(self):
        cursor = self.connection.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        return rows
    
    def transactions_amount(self):
        cursor = self.connection.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]
        return count