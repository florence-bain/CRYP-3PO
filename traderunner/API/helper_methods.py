
import datetime

def parse_time(time):
    readable_time = (datetime.datetime.fromtimestamp(time / 1000))
    return readable_time


