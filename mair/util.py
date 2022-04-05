from math import log, exp


def lin_get(min, max, val):
    return min + (max - min) * val


def lin_set(min, max, val):
    return (val - min) / (max - min)


def log_get(min, max, val):
    return min * exp(log(max / min) * val)


def log_set(min, max, val):
    return log(val / min) / log(max / min)


def _get_fader_val(retval):
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


def _set_fader_val(self, val):
    if val >= 10:
        self.setter("fader", 1)
    elif val >= -10:
        self.setter("fader", (val + 30) / 40)
    elif val >= -30:
        self.setter("fader", (val + 50) / 80)
    elif val >= -60:
        self.setter("fader", (val + 70) / 160)
    elif val >= -90:
        self.setter("fader", (val + 90) / 480)
    else:
        self.setter("fader", 0)


def _get_level_val(retval):
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


def _set_level_val(self, val):
    if val >= 10:
        self.setter("level", 1)
    elif val >= -10:
        self.setter("level", (val + 30) / 40)
    elif val >= -30:
        self.setter("level", (val + 50) / 80)
    elif val >= -60:
        self.setter("level", (val + 70) / 160)
    elif val >= -90:
        self.setter("level", (val + 90) / 480)
    else:
        self.setter("level", 0)
