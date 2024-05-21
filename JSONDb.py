import json
import os
from DbInterface import DbInterface

# Interfacen pohjalta määritellään JSONDatabase

class JSONDatabase(DbInterface):
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
    
    # Ei tarvita
    def create_tasks_table(self):
        pass

    def loadTasks(self, year, month, day):
        with open(self.filename, 'r') as f:
            tasks = json.load(f)
        tasksToReturn = [f"{task['time']}: {task['task']}" for task in tasks if task['year'] == year and task['month'] == month and task['day'] == day]
        return tasksToReturn

    def deleteOne(self, year, month, day, task, time):
        with open(self.filename, 'r') as f:
            tasks = json.load(f)
        # jättää pois ehdot täyttävät taskit
        tasks = [t for t in tasks if not (t['year'] == year and t['month'] == month and t['day'] == day and t['task'] == task and t['time'] == time)]
        # jonka jälkeen päivitetään json
        with open(self.filename, 'w') as f:
            json.dump(tasks, f)

    def sendOne(self, year, month, day, task, time):
        with open(self.filename, 'r') as f:
            tasks = json.load(f)
        tasks.append({"year": year, "month": month, "day": day, "task": task, "time": time})
        with open(self.filename, 'w') as f:
            json.dump(tasks, f)

    def deleteAll(self):
        with open(self.filename, 'w') as f:
            json.dump([], f)
    
    # Ei tarvita
    def close(self):
        pass