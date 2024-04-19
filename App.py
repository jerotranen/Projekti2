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

        # GUI:n ja koodin linkitys
        self.ui.calendarWidget.selectionChanged.connect(self.handle_date_selection)
        self.ui.pushButton.clicked.connect(self.deleteOne)
        self.ui.pushButton_2.clicked.connect(self.sendOne)
        self.ui.pushButton_3.clicked.connect(self.deleteAll)
        self.ui.horizontalSlider.valueChanged.connect(self.handle_slider_change)
        self.ui.horizontalSlider.setMaximum(23)
        self.task_model = QStringListModel()
        self.ui.listView.setModel(self.task_model)
        self.ui.listView.clicked.connect(self.handle_task_click)
        self.conn = sqlite3.connect('tasks.db')
        self.cur = self.conn.cursor()
        
        #Säädatan haku alussa, jotta API ei kuormitu
        self.hourly_weather_data = Weather.fetchWeather()

        self.selected_task = None

        # Jos tablea ei ole eli siis voi poistaa kun on pysyvä db
        self.create_tasks_table()

    def create_tasks_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                year INTEGER,
                month INTEGER,
                day INTEGER,
                task TEXT,
                time TEXT
            )
        ''')
        self.conn.commit()
    
    # Funktio joka näyttää haetun säädatan käyttöliittymässä seuraavan 14 päivän aikana
    def weathertest(self, slider_value, selected_date):
        today = QDate.currentDate()
        if selected_date < today or selected_date > today.addDays(14):

            self.ui.label.setText("Weather N/A")
            self.ui.label_2.setText("")
            self.ui.label_3.setText("")
            self.ui.label_4.setText("")
            return

        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()

        if 'date' not in self.hourly_weather_data.index.names:
            self.hourly_weather_data.set_index('date', inplace=True)
        
        selected_hour_data = self.hourly_weather_data[
            (self.hourly_weather_data.index.year == year) &
            (self.hourly_weather_data.index.month == month) &
            (self.hourly_weather_data.index.day == day)]   

        if slider_value < 0 or slider_value >= len(selected_hour_data):
            self.ui.label.setText("Weather N/A")
            self.ui.label_2.setText("")
            self.ui.label_3.setText("")
            self.ui.label_4.setText("")
            return

        selected_hour_data = selected_hour_data.iloc[slider_value]

        selected_hour = selected_hour_data.name.strftime("%H:%M")
        temp = "{:.1f}".format(selected_hour_data['temperature_2m'])
        wind_speed = "{:.1f}".format(selected_hour_data['wind_speed_10m'])
        rain = "{:.1f}".format(selected_hour_data['rain'])
        uv_index = "{:.1f}".format(selected_hour_data['uv_index'])

        self.ui.label.setText(f'Temp: {temp}°C\n at {selected_hour}')
        self.ui.label_2.setText(f'Wind: {wind_speed} m/s\n at {selected_hour}')
        self.ui.label_3.setText(f'Rain: {rain} mm\n at {selected_hour}')
        self.ui.label_4.setText(f'UV: {uv_index}\n at {selected_hour}')


    # Kellonajan valinta säädatalle
    def handle_slider_change(self, value):
        selected_date = self.ui.calendarWidget.selectedDate()
        self.weathertest(value, selected_date)

    # Yksittäisen tehtävän valitseminen
    def handle_task_click(self, index):
        self.selected_task = self.task_model.data(index, Qt.DisplayRole)

    # Yksittäisen tehtävän poistaminen valitsemisen jälkeen
    def deleteOne(self):
        if self.selected_task:
            # Koska selected_task on time + task, niin erotetaan ne toisistaan, jotta SQL toimii oikein
            # Muuten yksittäistä taskia ei voi jostain syystä poistaa vain päivämäärällä(?)
            selected_time, selected_task = self.selected_task.split(': ', 1)
            selected_date = self.ui.calendarWidget.selectedDate()
            year = selected_date.year()
            month = selected_date.month()
            day = selected_date.day()
            self.cur.execute("DELETE FROM tasks WHERE time=? AND task=? AND year=? AND month=? AND day=?", (selected_time, selected_task, year, month, day))
            self.conn.commit()
            self.handle_date_selection()
            self.selected_task = None

    # Päivän valitseminen kalenterista
    def handle_date_selection(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        self.cur.execute("SELECT task, time FROM tasks WHERE year=? AND month=? AND day=? ORDER BY time", (year, month, day))
        task_data = self.cur.fetchall()
        tasks_with_time = [f"{row[1]}: {row[0]}" for row in task_data]  # Concatenate time with task
        self.task_model.setStringList(tasks_with_time)
        self.weathertest(0, selected_date)

    # Yhden tehtävän lisääminen päivälle
    def sendOne(self):
        text = self.ui.lineEdit.text()
        selected_time = self.ui.timeEdit.time().toString("HH:mm")
        tasks = []
        tasks.append(text)
        self.ui.lineEdit.clear()
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()

        self.cur.execute("INSERT INTO tasks (year, month, day, task, time) VALUES (?, ?, ?, ?, ?)", (year, month, day, text, selected_time))
        self.conn.commit()
        # Refreshaa lähettämisen jälkeen
        self.handle_date_selection()
    
    # Poistaa kaikki taskit kaikkialta
    def deleteAll(self):
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