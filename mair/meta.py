from .errors import MAirRemoteError
from .util import lin_get, lin_set


def bool_prop(param):
    """A boolean property object."""

    def fget(self):
        return self.getter(param)[0] == 1

    def fset(self, val):
        if not isinstance(val, bool):
            raise MAirRemoteError(f"{param} is a boolean parameter")
        self.setter(param, 1 if val else 0)

    return property(fget, fset)


def string_prop(param):
    """A string property object"""

    def fget(self):
        return self.getter(param)[0]

    def fset(self, val):
        if not isinstance(val, str):
            raise MAirRemoteError(f"{param} is a string parameter")
        self.setter(param, val)

    return property(fget, fset)


def int_prop(param):
    """An integer property object"""

    def fget(self):
        return int(self.getter(param)[0])

    def fset(self, val):
        if not isinstance(val, int):
            raise MAirRemoteError(f"{param} is an integer parameter")
        self.setter(param, val)

    return property(fget, fset)


def float_prop(param):
    """A float property object"""

    def fget(self):
        return round(self.getter(param)[0], 1)

    def fset(self, val):
        if not isinstance(val, int):
            raise MAirRemoteError(f"{param} is a float parameter")
        self.setter(param, val)

    return property(fget, fset)


def geq_prop(param):
    # fmt: off
    opts = {
        "1k": 1000, "1k25": 1250, "1k6": 1600, "2k": 2000, "3k15": 3150, "4k": 4000,
        "5k": 5000, "6k3": 6300, "8k": 8000, "10k": 10000, "12k5": 12500, "16k": 16000,
        "20k": 20000,
    }
    # fmt: on
    param = param.replace("_", ".")

    def fget(self) -> float:
        return round(lin_get(-15, 15, self.getter(param)[0]), 1)

    def fset(self, val):
        self.setter(param, lin_set(-15, 15, val))

    return property(fget, fset)
