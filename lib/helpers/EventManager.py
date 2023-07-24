import json

class EventManager:
    def __init__(self):
        self.uuid = ''
        self.last_time_read = -1
        self.showing_message = False
        self.ttl = 30
        self.period_check = 60

    def get(self):
        with open(f"/event.json", "r") as read_file:
            return json.load(read_file)
