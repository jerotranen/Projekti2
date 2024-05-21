from Weather import Weather
from JSONDb import JSONDatabase
from SQLDb import SQLiteDatabase

# Model luokka vastaa database-operaatioista, säädatan hakemisesta ja sen käsittelemisestä
# Ei ole riippuvainen GUI-luokasta, jolloin MVC -arkkitehtuuri toteutuu

class Model():
    def __init__(self, db_type):
        if db_type == 'sqlite':
            self.db = SQLiteDatabase()
        elif db_type == 'json':
            self.db = JSONDatabase()
        else:
            raise ValueError("Error with DB selection")

        # Säädata
        self.hourly_weather_data = Weather.fetchWeather()

    def create_tasks_table(self):
        self.db.create_tasks_table()
    
    def loadTasks(self, year, month, day):
        return self.db.loadTasks(year, month, day)

    def deleteOne(self, year, month, day, task, time):
            self.db.deleteOne(year, month, day, task, time)
            
    def sendOne(self, year, month, day, task, time):
        self.db.sendOne(year, month, day, task, time)
    
    def deleteAll(self):
        self.db.deleteAll()

    def returnHourlyData(self, hour, year, month, day):
        if 'date' not in self.hourly_weather_data.index.names:
            self.hourly_weather_data.set_index('date', inplace=True) # Date indexiksi df:een
        
        selected_hour_data = self.hourly_weather_data[
            (self.hourly_weather_data.index.year == year) &
            (self.hourly_weather_data.index.month == month) &
            (self.hourly_weather_data.index.day == day)]

        if hour < 0 or hour >= len(selected_hour_data):
            return("N/A")

        selected_hour_data = self.hourly_weather_data.iloc[hour] # iloc valitsee columnin tunnin perusteella
        selected_hour = selected_hour_data.name.strftime("%H:%M")
        temp = "{:.1f}".format(selected_hour_data['temperature_2m'])
        wind_speed = "{:.1f}".format(selected_hour_data['wind_speed_10m'])
        rain = "{:.1f}".format(selected_hour_data['rain'])
        uv_index = "{:.1f}".format(selected_hour_data['uv_index'])
        weather_code = selected_hour_data['weather_code']

        return {
            'temp': temp,
            'wind_speed': wind_speed,
            'rain': rain,
            'uv_index': uv_index,
            'weather_code': weather_code
        }