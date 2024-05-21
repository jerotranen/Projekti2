import sqlite3
from DbInterface import DbInterface

class SQLiteDatabase(DbInterface):
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cur = self.conn.cursor()

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

    def loadTasks(self, year, month, day):
        self.cur.execute("SELECT task, time FROM tasks WHERE year=? AND month=? AND day=? ORDER BY time", (year, month, day))
        loadedtasks = self.cur.fetchall()
        tasksToReturn = [f"{row[1]}: {row[0]}" for row in loadedtasks]
        return tasksToReturn

    def deleteOne(self, year, month, day, task, time):
        self.cur.execute("DELETE FROM tasks WHERE year=? AND month=? AND day=? AND task=? AND time=?", (year, month, day, task, time))
        self.conn.commit()
    
    def sendOne(self, year, month, day, task, time):
        self.cur.execute("INSERT INTO tasks (year, month, day, task, time) VALUES (?, ?, ?, ?, ?)", (year, month, day, task, time))
        self.conn.commit()

    def deleteAll(self):
        self.cur.execute("DELETE FROM tasks")
        self.conn.commit()

    def close(self):
        self.conn.close()