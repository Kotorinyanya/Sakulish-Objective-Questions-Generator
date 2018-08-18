import time
from datetime import datetime as dt


def timestamp():
    """
    Get Unix timestamp in int type.
    :return: timestamp
    """
    return int(time.time())


def datetime(time_stamp):
    """
    Get date string with Unix timestamp.
    :param time_stamp:
    :return: date string
    """
    return dt.fromtimestamp(
        int(time_stamp)
    ).strftime('%Y-%m-%d %H:%M:%S')


def counter(start=1, step=1):
    """
    Return a counter, each access it will increase [step].
    :param start: start number
    :param step: increment each call
    :return:
    """
    x = [start]

    def real_counter():
        now_count = x[0]
        x[0] += step
        return now_count
    return real_counter
