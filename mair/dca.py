import abc
from .errors import MAirRemoteError


class IDCA(abc.ABC):
    """Abstract Base Class for DCA groups"""

    def __init__(self, remote, index: int):
        self._remote = remote
        self.index = index + 1

    def getter(self, param: str) -> tuple:
        self._remote.send(f"{self.address}/{param}")
        return self._remote.info_response

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
        if not isinstance(val, bool):
            raise MAirRemoteError("on is a boolean parameter")
        self.setter("on", 1 if val else 0)

    @property
    def name(self) -> str:
        return self.getter("config/name")[0]

    @name.setter
    def name(self, val: str):
        if not isinstance(val, str):
            raise MAirRemoteError("name is a str parameter")
        self.setter("config/name")[0]

    @property
    def color(self) -> int:
        return self.getter("config/color")[0]

    @color.setter
    def color(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("color is an int parameter")
        self.setter("config/color", val)
