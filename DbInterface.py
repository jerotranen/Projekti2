#https://stackoverflow.com/questions/2124190/how-do-i-implement-interfaces-in-python
from abc import ABC, abstractmethod

# Rajapinta databaseja varten
# Metodit määritellään erikseen <db>.py fileissä
# Tämä tehdään, jotta Model-luokassa ei tarvitse määritellä mikä db kyseessä! Vaan se tehdään main.py:ssä
class DbInterface(ABC):

    @abstractmethod
    def create_tasks_table(self):
        pass

    @abstractmethod
    def loadTasks(self, year, month, day):
        pass

    @abstractmethod
    def deleteOne(self, year, month, day, task, time):
        pass

    @abstractmethod
    def sendOne(self, year, month, day, task, time):
        pass

    @abstractmethod
    def deleteAll(self):
        pass

    @abstractmethod
    def close(self):
        pass