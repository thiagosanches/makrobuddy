import json

UUID = "uuid"
MESSAGE = "message"


class EventManager:
    def __init__(self):
        self.uuid = ''
        self.last_time_read = -1
        self.showing_message = False
        self.ttl = 30
        self.period_check = 60

    def get(self):
        try:
            with open(f"/event.json", "r") as read_file:
                return json.load(read_file)
        except:
            return None

    def run(self, now) -> str:
        event_message = None
        if now >= (self.last_time_read + self.period_check) and not self.showing_message:
            event = self.get()
            if event != None:
                if event[UUID] != self.uuid:
                    self.uuid = event[UUID]
                    self.showing_message = True
                    self.last_time_read = now
                    event_message = event[MESSAGE]

        return event_message
