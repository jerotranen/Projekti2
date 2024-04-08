import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QStringListModel, QDate, Qt
from mainwin import Ui_MainWindow 
from Weather import Weather

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.calendarWidget.selectionChanged.connect(self.handle_date_selection)
        self.ui.pushButton.clicked.connect(self.handle_push_button)
        self.ui.pushButton_2.clicked.connect(self.handle_push_button2)
        self.ui.pushButton_3.clicked.connect(self.handle_delete_button)
        self.ui.horizontalSlider.valueChanged.connect(self.handle_slider_change)
        self.ui.horizontalSlider.setMaximum(23)
        self.task_model = QStringListModel()
        self.ui.listView.setModel(self.task_model)
        self.ui.listView.clicked.connect(self.handle_task_click)
        self.conn = sqlite3.connect('tasks.db')
        self.cur = self.conn.cursor()
        self.hourly_weather_data = Weather.fetchWeather()
        self.weathertest(0)

        self.selected_task = None
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
    
    def weathertest(self, slider_value):
        selected_hour_data = self.hourly_weather_data.iloc[slider_value]

        selected_hour = selected_hour_data['date'].strftime("%H:%M")
        temp = "{:.1f}".format(selected_hour_data['temperature_2m'])
        wind_speed = "{:.1f}".format(selected_hour_data['wind_speed_10m'])
        rain = "{:.1f}".format(selected_hour_data['rain'])
        uv_index = "{:.1f}".format(selected_hour_data['uv_index'])

        self.ui.label1.setText(f'Temp: {temp}°C\n at {selected_hour}')
        self.ui.label2.setText(f'Wind Speed: {wind_speed} m/s\n at {selected_hour}')
        self.ui.label3.setText(f'Rain: {rain} mm\n at {selected_hour}')
        self.ui.label4.setText(f'UV Index: {uv_index}\n at {selected_hour}')

    def handle_slider_change(self, value):
        self.weathertest(value)

    def handle_task_click(self, index):
        self.selected_task = self.task_model.data(index, Qt.DisplayRole)

    def handle_delete_button(self):
        if self.selected_task:
            selected_date = self.ui.calendarWidget.selectedDate()
            year = selected_date.year()
            month = selected_date.month()
            day = selected_date.day()
            self.cur.execute("DELETE FROM tasks WHERE task=? AND year=? AND month=? AND day=?", (self.selected_task, year, month, day))
            self.conn.commit()
            self.handle_date_selection()
            self.selected_task = None

    def handle_date_selection(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        self.cur.execute("SELECT task FROM tasks WHERE year=? AND month=? AND day=?", (year, month, day))
        tasks = [row[0] for row in self.cur.fetchall()]
        self.task_model.setStringList(tasks)

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

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()