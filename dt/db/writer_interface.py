from .interface import DatabaseConnection, DatabaseInterface
from pandas import DataFrame
from hashlib import sha256

class WriterDatabaseInterface(DatabaseInterface):
    def __init__(self, database_connection: DatabaseConnection) -> None:
        super().__init__(database_connection)

    def transactions_insert(self, transactions: DataFrame):
        try:
            transactions["id"] = transactions.apply(lambda row: sha256("".join(str(value) for value in row).encode()).hexdigest(), axis=1)
            transactions.drop_duplicates(subset=["id"], inplace=True)
            transactions.to_sql("transactions", self.connection, if_exists="append", index=False)
        except Exception as e:
            print(type(e).__name__)

            raise Exception(f"Error inserting transactions into database: {e}")