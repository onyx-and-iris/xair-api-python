import abc
from typing import Optional

from .errors import XAirRemoteError
from .meta import mute_prop
from .shared import EQ, GEQ, Automix, Config, Dyn, Gate, Group, Insert, Mix, Preamp


class ILR(abc.ABC):
    """Abstract Base Class for buses"""

    def __init__(self, remote, index: Optional[int] = None):
        self._remote = remote
        if index is not None:
            self.index = index + 1

    def getter(self, param: str):
        return self._remote.query(f"{self.address}/{param}")

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class LR(ILR):
    """Concrete class for buses"""

    @classmethod
    def make(cls, remote, index=None):
        """
        Factory function for LR

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns an LR class of a kind.
        """
        LR_cls = type(
            f"LR{remote.kind}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (
                        Config,
                        Dyn,
                        Insert,
                        GEQ.make(),
                        EQ.make_sixband(cls, remote, index),
                        Mix,
                    )
                },
                "mute": mute_prop(),
            },
        )
        return LR_cls(remote, index)

    @property
    def address(self) -> str:
        return f"/lr"
