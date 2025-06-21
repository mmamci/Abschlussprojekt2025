from datetime import datetime

class AutoNotification:
    def __init__(self, intervall, start_time):
        self.intervall = intervall
        self.start_time = start_time
        self.last_check = datetime.now()
    
    def check_time():
        pass

    def notify():
        pass

class Variable:
    def __init__(self, name, notification, goal):
        self.name = name
        self.notification = notification
        self.goal = goal


notif = AutoNotification("Daily", datetime.now())

print(notif.last_check)