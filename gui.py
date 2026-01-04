#!.dt-venv/bin/python3
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QTableWidget,
)
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

        self.setWindowTitle("Data Transformer")
        self.setMinimumSize(QSize(width // 2 , height // 2))

        table = DTTable()
        table.setRowCount(10)
        table.setColumnCount(5)

        self.addToolBar(DTToolbar(self))

        self.setCentralWidget(table)


window = DTMainWindow()
window.show()

app.exec()