import abc

from .errors import XAirRemoteError
from .meta import mute_prop
from .shared import EQ, GEQ, Automix, Config, Dyn, Gate, Group, Insert, Mix, Preamp


class IFX(abc.ABC):
    """Abstract Base Class for fxs"""

    def __init__(self, remote, index: int):
        self._remote = remote
        self.index = index + 1

    def getter(self, param: str):
        return self._remote.query(f"{self.address}/{param}")

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class FX(IFX):
    """Concrete class for fx"""

    @property
    def address(self) -> str:
        return f"/fx/{self.index}"

    @property
    def type(self) -> int:
        return self.getter("type")[0]

    @type.setter
    def type(self, val: int):
        self.setter("type", val)


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
            f"FXSend{remote.kind}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (Config, Mix, Group)
                },
                "mute": mute_prop(),
            },
        )
        return FXSEND_cls(remote, index)

    @property
    def address(self) -> str:
        return f"/fxsend/{self.index}"
