import datetime

import pytz


class CustomizeTime():
    def __init__(self, timezone):
        self.timezone = pytz.timezone(timezone)

    def now(self):
        return datetime.datetime.now(self.timezone)

    def datetime(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        return datetime.datetime(year, month, day, hour, minute, second, tzinfo=self.timezone)

    def fromtimestamp(self, timestamp):
        return str(datetime.datetime.fromtimestamp(timestamp, self.timezone)).split('.')[0]


customize_time = CustomizeTime('Asia/Taipei')