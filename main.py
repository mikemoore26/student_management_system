import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)

        file_menu_item = self.menuBar().addMenu("&File")
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        help_menu_item = self.menuBar().addMenu("&Help")
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        edit_menu_item = self.menuBar().addMenu("&Edit")
        search_student_action = QAction(QIcon("icons/search.png"),"search Student", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)


        #Add toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)
        self.load_data()

        #ADD Status bar

    def load_data(self):
        connection = sqlite3.Connection("database.db")
        res = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for index_r, row in enumerate(res):
            self.table.insertRow(index_r)
            for index_c, col in enumerate(row):
                self.table.setItem(index_r, index_c, QTableWidgetItem(str(col)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student")
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        layout = QVBoxLayout()
        #
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = "Biology Math Astronomy Physics".split()
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # MObile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("mobile #")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(self.addStudent)
        layout.addWidget(button)

        self.setLayout(layout)

    def addStudent(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.Connection("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES (?,?,?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("name")
        layout.addWidget(self.name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)
        self.setLayout(layout)

    def search(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        sql = "SELECT * FROM students WHERE name=?"
        res = cursor.execute(sql, (self.name.text(),))
        rows = list(res)
        print(rows)
        items = window.table.findItems(self.name.text(), Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()
        pass


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()
    app.exit(sys.exit())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()
    app.exit(sys.exit())
