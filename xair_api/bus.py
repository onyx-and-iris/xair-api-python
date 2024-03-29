import abc
import logging

from .meta import mute_prop
from .shared import EQ, GEQ, Config, Dyn, Group, Insert, Mix

logger = logging.getLogger(__name__)


class IBus(abc.ABC):
    """Abstract Base Class for buses"""

    def __init__(self, remote, index: int):
        self._remote = remote
        self.index = index + 1
        self.logger = logger.getChild(self.__class__.__name__)

    def getter(self, param: str):
        return self._remote.query(f"{self.address}/{param}")

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class Bus(IBus):
    """Concrete class for buses"""

    @classmethod
    def make(cls, remote, index):
        """
        Factory function for buses

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns a Bus class of a kind.
        """
        BUS_cls = type(
            f"Bus{remote.kind}",
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
                        Group,
                    )
                },
                "mute": mute_prop(),
            },
        )
        return BUS_cls(remote, index)

    @property
    def address(self) -> str:
        return f"/bus/{self.index}"
