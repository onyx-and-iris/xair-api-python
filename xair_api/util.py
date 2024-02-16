import functools
import time
from math import exp, log

from .errors import XAirRemoteConnectionTimeoutError


def timeout(func):
    """
    Times out the login function once time elapsed exceeds remote.connect_timeout.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        remote, *_ = args

        err = None
        start = time.time()
        while time.time() < start + remote.connect_timeout:
            try:
                func(*args, **kwargs)
                remote.logger.debug(f"login time: {round(time.time() - start, 2)}")
                err = None
                break
            except XAirRemoteConnectionTimeoutError as e:
                err = e
                continue
        if err:
            raise err

    return wrapper


def lin_get(min, max, val):
    return min + (max - min) * val


def lin_set(min, max, val):
    return (val - min) / (max - min)


def log_get(min, max, val):
    return min * exp(log(max / min) * val)


def log_set(min, max, val):
    return log(val / min) / log(max / min)


def db_from(func):
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


def db_to(func):
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
