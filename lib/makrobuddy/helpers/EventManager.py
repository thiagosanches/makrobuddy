import json
import rtc
import time

UUID = "uuid"
MESSAGE = "message"
DATE = "date"

class EventManager:
    def __init__(self):
        self.uuid = ''
        self.last_time_read = -1
        self.showing_message = False
        self.ttl = 30
        self.period_check = 60
        self.rtc = rtc.RTC()
        self.time = None

    def get(self):
        try:
            with open(f"/event.json", "r") as read_file:
                return json.load(read_file)
        except:
            return None

    def sync_clock(self, datetime: str):
        year = int(datetime[:4])
        month = int(datetime[5:7])
        day = int(datetime[8:10])
        hour = int(datetime[11:13])
        minute = int(datetime[14:16])
        second = int(datetime[17:19])
        return time.struct_time((year, month, day, hour, minute, second, 0, 0, -1))

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

                    if self.time == None:
                        print("[EventManager] I'm going to set the internal clock based on the first event received!")
                        self.rtc.datetime = self.sync_clock(event[DATE])
                        print("[EventManager] " + str(self.rtc.datetime))

        return event_message