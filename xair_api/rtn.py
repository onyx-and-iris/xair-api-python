import abc
from typing import Optional

from .errors import XAirRemoteError
from .meta import mute_prop
from .shared import EQ, GEQ, Automix, Config, Dyn, Gate, Group, Insert, Mix, Preamp


class IRtn(abc.ABC):
    """Abstract Base Class for aux"""

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


class AuxRtn(IRtn):
    """Concrete class for aux"""

    @classmethod
    def make(cls, remote, index=None):
        """
        Factory function for auxrtn
        Creates a mixin of shared subclasses, sets them as class attributes.
        Returns an AuxRtn class of a kind.
        """
        AUXRTN_cls = type(
            f"AuxRtn{remote.kind}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (
                        Config,
                        Preamp,
                        EQ.make_fourband(cls, remote),
                        Mix,
                        Group,
                    )
                },
                "mute": mute_prop(),
            },
        )
        return AUXRTN_cls(remote, index)

    @property
    def address(self):
        return "/rtn/aux"


class FxRtn(IRtn):
    """Concrete class for rtn"""

    @classmethod
    def make(cls, remote, index):
        """
        Factory function for fxrtn
        Creates a mixin of shared subclasses, sets them as class attributes.
        Returns an FxRtn class of a kind.
        """
        FXRTN_cls = type(
            f"FxRtn{remote.kind}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (
                        Config,
                        Preamp,
                        EQ.make_fourband(cls, remote, index),
                        Mix,
                        Group,
                    )
                },
                "mute": mute_prop(),
            },
        )
        return FXRTN_cls(remote, index)

    @property
    def address(self):
        return f"/rtn/{self.index}"
