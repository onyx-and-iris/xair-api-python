import abc


class IDCA(abc.ABC):
    """Abstract Base Class for DCA groups"""

    def __init__(self, remote, index: int):
        self._remote = remote
        self.index = index + 1

    def getter(self, param: str) -> tuple:
        return self._remote.query(f"{self.address}/{param}")

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class DCA(IDCA):
    """Concrete class for DCA groups"""

    @property
    def address(self) -> str:
        return f"/dca/{self.index}"

    @property
    def on(self) -> bool:
        return self.getter("on")[0] == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    def mute(self) -> bool:
        return not self.on

    @mute.setter
    def mute(self, val: bool):
        self.on = not val

    @property
    def name(self) -> str:
        return self.getter("config/name")[0]

    @name.setter
    def name(self, val: str):
        self.setter("config/name", val)

    @property
    def color(self) -> int:
        return self.getter("config/color")[0]

    @color.setter
    def color(self, val: int):
        self.setter("config/color", val)
