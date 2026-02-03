from datetime import datetime
from hashlib import sha256
from dt.io.db.interface import DatabaseInterface
from pandas import DataFrame

class TransactionList:
    def __init__(self):
        self.transactions: list[Transaction] = []

    @classmethod
    def from_dataframe(cls, df):
        transaction_list = cls()
        for _, row in df.iterrows():
            transaction = Transaction(
                date=row['date'],
                description=row['description'],
                institution=row['institution'],
                type=row['type'],
                amount=row['amount']
            )
            transaction_list.add_transaction(transaction)
        return transaction_list

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def remove_transaction(self, id: str):
        self.transactions = [t for t in self.transactions if t.id != id]

    def write_to_db(self, db: DatabaseInterface, verbose: bool = False):
        transactions_added = 0
        transactions_skipped = 0
        for transaction in self.transactions:
            if  db.transactions_search(transaction.id) is None:
                db.connection.execute(
                    """
                    INSERT INTO transactions (id, date, description, institution, type, amount)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (transaction.id, transaction.date.isoformat(), transaction.description, transaction.institution, transaction.type, transaction.amount)
                )
                db.connection.commit()
                transactions_added += 1
            else:
                transactions_skipped += 1

        if verbose:
            print(f"Transactions added: {transactions_added}")
            print(f"Transactions skipped (duplicates): {transactions_skipped}")

    def write_to_csv(self, file_path: str, append: bool = False, verbose: bool = False):
        df = DataFrame([{
            'id': t.id,
            'date': t.date,
            'description': t.description,
            'institution': t.institution,
            'type': t.type,
            'amount': t.amount
        } for t in self.transactions])

        df.to_csv(
            file_path,
            index=False,
            float_format="%.2f",
            date_format="%Y-%m-%d",
            header=append is False,
            mode="a" if append is True else "w"
        )

        if verbose:
            print(f"Wrote {len(self.transactions)} transactions to {file_path}")

    def __str__(self) -> str:
        return "\n".join(str(t) for t in self.transactions)

class Transaction:
    def __init__(self, date: datetime, description: str, institution: str, type: str, amount: float):
        self.id = sha256(f"{date}{description}{institution}{type}{amount}".encode('utf-8')).hexdigest()
        self.date = date
        self.description = description
        self.institution = institution
        self.type = type
        self.amount = amount
    
    def __str__(self) -> str:
        return f"Transaction(id={self.id}, date={self.date}, description={self.description}, institution={self.institution}, type={self.type}, amount={self.amount})"
