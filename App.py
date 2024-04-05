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
        self.ui.pushButton.clicked.connect(self.handle_push_button)
        self.ui.pushButton_2.clicked.connect(self.handle_push_button2)
        self.task_model = QStringListModel()
        self.ui.listView.setModel(self.task_model)
        self.ui.listView.clicked.connect(self.handle_task_click)
        self.conn = sqlite3.connect('tasks.db')
        self.cur = self.conn.cursor()

        # Jos tablea ei ole eli siis voi poistaa kun on pysyvä db
        self.create_tasks_table()

    def create_tasks_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                year INTEGER,
                month INTEGER,
                day INTEGER,
                task TEXT
            )
        ''')
        self.conn.commit()

    def handle_date_selection(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        print(selected_date)
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        self.cur.execute("SELECT task FROM tasks WHERE year=? AND month=? AND day=?", (year, month, day))
        tasks = [row[0] for row in self.cur.fetchall()]
        self.task_model.setStringList(tasks)
    
    def handle_task_click(self, index):
        selected_task = self.task_model.data(index, Qt.DisplayRole)
        print(f"Selected task: {selected_task}")
        self.cur.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
        self.conn.commit()
        self.handle_date_selection()

    # Yhden task lisääminen päivälle
    def handle_push_button(self):
        text = self.ui.lineEdit.text()
        tasks = []
        tasks.append(text)
        self.ui.lineEdit.clear()
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()

        self.cur.execute("INSERT INTO tasks (year, month, day, task) VALUES (?, ?, ?, ?)", (year, month, day, text))
        self.conn.commit()

        # Refreshaa lähettämisen jälkeen
        self.handle_date_selection()
    
    # Poistaa kaikki taskit kaikkialta
    def handle_push_button2(self):
        self.cur.execute("DELETE FROM tasks")
        self.conn.commit()
        self.handle_date_selection()


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