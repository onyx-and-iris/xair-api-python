import abc
from .errors import MAirRemoteError
from .shared import (
    Config,
    Preamp,
    Gate,
    Dyn,
    Insert,
    EQ,
    GEQ,
    Mix,
    Group,
    Automix,
)


class IFX(abc.ABC):
    """Abstract Base Class for fxs"""

    def __init__(self, remote, index: int):
        self._remote = remote
        self.index = index + 1

    def getter(self, param: str):
        self._remote.send(f"{self.address}/{param}")
        return self._remote.info_response

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class FXSend(IFX):
    """Concrete class for fxsend"""

    @classmethod
    def make(cls, remote, index):
        """
        Factory function for FXSend

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns an FXSend class of a kind.
        """
        FXSEND_cls = type(
            f"FXSend{remote.kind.id_}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind.id_}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (Config, Mix, Group)
                }
            },
        )
        return FXSEND_cls(remote, index)

    @property
    def address(self) -> str:
        return f"/fxsend/{self.index}"


class FXReturn(IFX):
    """Concrete class for fxreturn"""

    @property
    def address(self) -> str:
        return f"/fx/{self.index}"

    @property
    def type(self) -> int:
        return self.getter("type")[0]

    @type.setter
    def type(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("type is an integer parameter")
        self.setter("type", val)
