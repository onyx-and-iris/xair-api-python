import abc

from .meta import mute_prop
from .shared import EQ, Automix, Config, Dyn, Gate, Group, Insert, Mix, Preamp, Send


class IStrip(abc.ABC):
    """Abstract Base Class for strips"""

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


class Strip(IStrip):
    """Concrete class for strips"""

    @classmethod
    def make(cls, remote, index):
        """
        Factory function for strips

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns a Strip class of a kind.
        """

        STRIP_cls = type(
            f"Strip{remote.kind}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind}", (_cls, cls), {}
                    )(remote, index)
                    for _cls in (
                        Config,
                        Preamp,
                        Gate,
                        Dyn,
                        Insert,
                        EQ.make_fourband(cls, remote, index),
                        Mix,
                        Group,
                        Automix,
                    )
                },
                "send": tuple(
                    Send.make(cls, i, remote, index)
                    for i in range(remote.kind.num_bus + remote.kind.num_fx)
                ),
                "mute": mute_prop(),
            },
        )
        return STRIP_cls(remote, index)

    @property
    def address(self) -> str:
        return f"/ch/{str(self.index).zfill(2)}"
