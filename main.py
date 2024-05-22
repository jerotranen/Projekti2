import sys
import threading
import Notification
import Model
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDate
from Gui import Gui
from Controller import Controller

# Notifikaatioille oma threadi
# pitäisi pyöriä, vaikka mainwindow suljetaan TODO: testaa vielä tämä. toimi ennen MVC
def start_notification_thread(tasksToRemind):
    threading.Thread(target=Notification.main, args=(tasksToRemind,)).start()

if __name__ == "__main__":
    # Kysytään käyttäjältä ennen sovelluksen käynnistämistä, mitä db tulisi käyttää
    db_type = input("Enter Database type (sqlite/json)".strip())
    # Controller -luokkaan asetetaan syötetty db_type
    Controller.set_db_type(db_type)
    app = QApplication(sys.argv)
    window = Gui()
    window.show()
    controller = Controller()
    # Ja vielä Model -luokkaan db_type. HUOM! Tähän se tulee konstruktoriin
    model = Model.Model(db_type=db_type)
    today = QDate.currentDate()
    year = today.year()
    month = today.month()
    day = today.day()
    # Notification threadia varten tämän päivän taskit
    model.create_tasks_table()
    tasksToRemind = model.loadTasks(year, month, day)
    # Ja käynnistetään thread
    start_notification_thread(tasksToRemind)
    sys.exit(app.exec_())