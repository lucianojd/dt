#!.dt-venv/bin/python3
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QTableWidget,
    QTableWidgetItem
)

from dt.db.interface import DatabaseConnection
from dt.db.reader_interface import ReaderDatabaseInterface
import sys

app = QApplication(sys.argv)
primary_screen = app.primaryScreen()
height = primary_screen.size().height() if primary_screen else 600
width = primary_screen.size().width() if primary_screen else 800


class DTTable(QTableWidget):
    def __init__(self):
        super().__init__()


class DTToolbar(QToolBar):
    def __init__(self, window):
        super().__init__("Main Window Toolbar")
        self.setIconSize(QSize(16, 16))

        menu = window.menuBar()
        file_menu = menu.addMenu("File")


class DTMainWindow(QMainWindow):
    def show_state(self, state):
        print(state == Qt.CheckState.Checked)
        print(state)

    def __init__(self):
        super().__init__()

        dbc = DatabaseConnection(sys.argv[0])
        dbc.init_db()
        rdbi = ReaderDatabaseInterface(dbc)

        self.setWindowTitle("Data Transformer")
        self.setMinimumSize(QSize(width // 2 , height // 2))

        transaction_count = rdbi.transactions_amount()
        transactions = rdbi.transactions_fetch_all()

        table = QTableWidget(transaction_count, 5)
        table.setHorizontalHeaderLabels(["Date", "Description", "Institution", "Type", "Amount"])
        
        for index, transaction in enumerate(transactions):
            dateItem = QTableWidgetItem(transaction[1])
            descriptionItem = QTableWidgetItem(transaction[2])
            institutionItem = QTableWidgetItem(transaction[3])
            typeItem = QTableWidgetItem(transaction[4])
            amountItem = QTableWidgetItem(str(transaction[5]))

            table.setItem(index, 0, dateItem)
            table.setItem(index, 1, descriptionItem)
            table.setItem(index, 2, institutionItem)
            table.setItem(index, 3, typeItem)
            table.setItem(index, 4, amountItem)
        
        table.show()

        self.addToolBar(DTToolbar(self))

        self.setCentralWidget(table)


window = DTMainWindow()
window.show()

app.exec()