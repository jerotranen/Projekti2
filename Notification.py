import time
import sched
from plyer import notification

def main(tasksToRemind):

    # Metodi notifikaatioille
    def remindMe(task_time, task_desc):
        notification.notify(
            title=f"Task Reminder at {task_time}",
            message=task_desc,
            timeout=6,
            app_name="App",
            app_icon=None,
            ticker="Task Reminder",
            toast=False
        )

    # Lista johonka tallennetaan kaikki päivän muistutukset threadin startattua
    reminders = []
    # Alustetaan scheduler
    s = sched.scheduler(time.time, time.sleep)
    current_time = time.time()
    current_hour = time.localtime(current_time).tm_hour
    current_minute = time.localtime(current_time).tm_min

    # Muunnetaan parametrina saatu lista käytettävämpään muotoon -> reminders-listaan
    for task in tasksToRemind:
        hour, minute, task_desc = task.split(':')
        task_hour, task_minute = int(hour), int(minute)
        task_time = f"{task_hour:02d}:{task_minute:02d}"
        reminder_time = current_time + ((task_hour - current_hour) * 3600) + ((task_minute - current_minute - 1) * 60)
        reminders.append((reminder_time, task_time, task_desc))

    # Jokainen reminder saa oman schedulerinsa
    for reminder in reminders:
        reminder_time, task_time, task_desc = reminder
        s.enterabs(reminder_time, 1, remindMe, argument=(task_time, task_desc))
    # Runnaa schedulerit
    s.run()