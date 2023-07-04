from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QToolBar, QTableWidget
from PyQt6.QtGui import QAction
import sys
from datetime import datetime


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management   System")

        file_menu_item = self.menuBar().addMenu("&File")
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        help_menu_item = self.menuBar().addMenu("&Help")
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name","Course", "Mobile"))
        self.setCentralWidget(self.table)

    def load_data(self):
        self.table
def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()
    app.exit(sys.exit())

if __name__ == "__main__":
    main()