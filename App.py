import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QStringListModel, QDate, Qt
from mainwin import Ui_MainWindow 

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.calendarWidget.selectionChanged.connect(self.handle_date_selection)
        self.task_model = QStringListModel()
        self.ui.listView.setModel(self.task_model)

    def handle_date_selection(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        print(selected_date)
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        tasks = ["task1", "task2"]
        dateobj = Date(year, month, day, tasks)
        self.task_model.setStringList(dateobj.tasks)

class Date:
    def __init__(self, year, month, day, tasks):
        self.year = year
        self.month = month
        self.day = day
        self.tasks = tasks

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()