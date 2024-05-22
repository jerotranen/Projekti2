import Model
import Gui

class Controller:
    model = None # Täytyy tehä initin ulkopuolella, jotta voidaan välttää selfin käyttö parametrinä! Hyvin tärkeää

    # Metodia voidaan käyttää muokkaamaan luokan variable ^
    @classmethod
    def set_db_type(cls, db_type):
        cls.model = Model.Model(db_type=db_type)

    def __init__(self):
        self.view = Gui.Gui()

    def handle_date_selection(year, month, day):
        tasks = Controller.model.loadTasks(year, month, day) # Käytetään suoraan modelia näin, jotta kun kutsutaan Gui:sta kutsut eivät mene sekaisin, liittyy ylempiin kommentteihin
        return tasks

    def deleteOne(year, month, day, task, time):
        Controller.model.deleteOne(year, month, day, task, time)

    def deleteAll():
        Controller.model.deleteAll()

    def sendOne(year, month, day, task, time):
        Controller.model.sendOne(year, month, day, task, time)
    
    def handle_slider_change(value, year, month, day):
        weatherData = Controller.model.returnHourlyData(value, year, month, day)
        if weatherData == "N/A":
            return "N/A"
        return [
            weatherData['temp'],
            weatherData['wind_speed'],
            weatherData['rain'],
            weatherData['uv_index'],
            weatherData['weather_code']
        ]
