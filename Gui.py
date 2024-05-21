from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwin import Ui_MainWindow
import Controller

# Tässä luokassa UI-elementtien yhdistäminen sovelluslogiikkaan
# Ei suoraa vaikutusta Model-luokkaan, joten saadaan aikaiseksi MVC-arkkitehtuuri

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller = Controller.Controller
        
        self.ui.calendarWidget.selectionChanged.connect(self.handle_date_selection)
        self.ui.pushButton.clicked.connect(self.deleteOne)
        self.ui.pushButton_2.clicked.connect(self.sendOne)
        self.ui.pushButton_3.clicked.connect(self.deleteAll)
        self.ui.horizontalSlider.valueChanged.connect(self.handle_slider_change)
        self.ui.horizontalSlider.setMaximum(23)
        self.task_model = QStringListModel()
        self.ui.listView.setModel(self.task_model)
        self.ui.listView.clicked.connect(self.handle_task_click)

        self.selected_task = None
        self.handle_slider_change(12)

    def handle_date_selection(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        tasksToShow = self.controller.handle_date_selection(year, month, day)
        self.task_model.setStringList(tasksToShow)
        self.handle_slider_change(12)

    def handle_slider_change(self, value):
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        returnedData = self.controller.handle_slider_change(value, year, month, day)
        if (returnedData != "N/A"):
            temp = returnedData[0]
            wind_speed = returnedData[1]
            rain = returnedData[2]
            uv_index = returnedData[3]
            weather_code = returnedData[4]
            self.ui.label.setText(f'Temp: {temp}°C\n at {value}')
            self.ui.label_2.setText(f'Wind: {wind_speed} m/s\n at {value}')
            self.ui.label_3.setText(f'Rain: {rain} mm\n at {value}')
            self.ui.label_4.setText(f'UV: {uv_index}\n at {value}')
            self.update_weather_image(weather_code, value)
        else:
            self.ui.label.setText('N/A')
            self.ui.label_2.setText('')
            self.ui.label_3.setText('')
            self.ui.label_4.setText('')

    def update_weather_image(self, weather_code, value):
        is_day = 6 <= value < 18 

        weather_code_int = int(weather_code)
        print(weather_code_int)
        if weather_code_int == 0:
            image_path = "./resources/sun.png" if is_day else "./resources/night.png"
        elif weather_code_int in (1, 2):
            image_path = "./resources/cloudy.png" if is_day else "./resources/cloudy-night.png"
        elif weather_code_int == 3:
            image_path = "./resources/cloud.png"
        elif 50 < weather_code_int < 86:
            image_path = "./resources/raining.png"
        elif weather_code_int >= 90:
            image_path = "./resources/thunderstorm.png"
        else:
            print("Weather icon yet to be introduced")
            return

        image_url = QtCore.QUrl.fromLocalFile(image_path)
        self.finalize_weather_image(image_url)
        
    def finalize_weather_image(self, image_url):
        pixmap = QtGui.QPixmap()
        pixmap.load(image_url.toLocalFile())
        scene = QtWidgets.QGraphicsScene()
        pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)
        self.ui.small_graphicsView.setScene(scene)

    def handle_task_click(self, index):
        self.selected_task = self.task_model.data(index, Qt.DisplayRole)

    def deleteOne(self):
        if self.selected_task:
            selected_date = self.ui.calendarWidget.selectedDate()
            year = selected_date.year()
            month = selected_date.month()
            day = selected_date.day()
            selected_time, selected_task = self.selected_task.split(': ', 1)
            self.controller.deleteOne(year, month, day, selected_task, selected_time)
            self.selected_task = None
            self.handle_date_selection()

    def deleteAll(self):
        self.controller.deleteAll()
        self.selected_task = None
        self.handle_date_selection()

    def sendOne(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        task = self.ui.lineEdit.text()
        time = self.ui.timeEdit.time().toString("HH:mm")
        self.controller.sendOne(year, month, day, task, time)
        self.ui.lineEdit.clear()
        self.handle_date_selection()