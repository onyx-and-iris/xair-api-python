import abc
from typing import Optional

from .errors import XAirRemoteError
from .shared import EQ, GEQ, Automix, Config, Dyn, Gate, Group, Insert, Mix, Preamp


class IRtn(abc.ABC):
    """Abstract Base Class for aux"""

    def __init__(self, remote, index: Optional[int] = None):
        self._remote = remote
        if index is not None:
            self.index = index + 1

    def getter(self, param: str):
        self._remote.send(f"{self.address}/{param}")
        return self._remote.info_response

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class Aux(IRtn):
    """Concrete class for aux"""

    @classmethod
    def make(cls, remote):
        """
        Factory function for aux

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns an Aux class of a kind.
        """
        AUX_cls = type(
            f"Aux{remote.kind}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind}", (_cls, cls), {}
                    )(remote)
                    for _cls in (
                        Config,
                        Preamp,
                        EQ.make_fourband(cls, remote),
                        Mix,
                        Group,
                    )
                }
            },
        )
        return AUX_cls(remote)

    @property
    def address(self):
        return "/rtn/aux"


class Rtn(IRtn):
    """Concrete class for rtn"""

    @classmethod
    def make(cls, remote, index):
        """
        Factory function for rtn

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns an Rtn class of a kind.
        """
        RTN_cls = type(
            f"Rtn{remote.kind.id_}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind.id_}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (
                        Config,
                        Preamp,
                        EQ.make_fourband(cls, remote, index),
                        Mix,
                        Group,
                    )
                }
            },
        )
        return RTN_cls(remote, index)

    @property
    def address(self):
        return f"/rtn/{self.index}"
