import functools
from math import exp, log


def lin_get(min, max, val):
    return min + (max - min) * val


def lin_set(min, max, val):
    return (val - min) / (max - min)


def log_get(min, max, val):
    return min * exp(log(max / min) * val)


def log_set(min, max, val):
    return log(val / min) / log(max / min)


def from_db(func):
    """fader|level converter for getters"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        retval = func(*args, **kwargs)

        if retval >= 1:
            return 10
        elif retval >= 0.5:
            return round((40 * retval) - 30, 1)
        elif retval >= 0.25:
            return round((80 * retval) - 50, 1)
        elif retval >= 0.0625:
            return round((160 * retval) - 70, 1)
        elif retval >= 0:
            return round((480 * retval) - 90, 1)
        else:
            return -90

    return wrapper


def to_db(func):
    """fader|level converter for setters"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        param, val = args
        if val >= 10:
            val = 1
        elif val >= -10:
            val = (val + 30) / 40
        elif val >= -30:
            val = (val + 50) / 80
        elif val >= -60:
            val = (val + 70) / 160
        elif val >= -90:
            val = (val + 90) / 480
        else:
            val = 0

        func(param, val, **kwargs)

    return wrapper
