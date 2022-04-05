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


class ILR(abc.ABC):
    """Abstract Base Class for buses"""

    def __init__(self, remote):
        self._remote = remote

    def getter(self, param: str):
        self._remote.send(f"{self.address}/{param}")
        return self._remote.info_response

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class LR(ILR):
    """Concrete class for buses"""

    @classmethod
    def make(cls, remote):
        """
        Factory function for LR

        Creates a mixin of shared subclasses, sets them as class attributes.

        Returns an LR class of a kind.
        """
        LR_cls = type(
            f"LR{remote.kind.id_}",
            (cls,),
            {
                **{
                    _cls.__name__.lower(): type(
                        f"{_cls.__name__}{remote.kind.id_}", (_cls, cls), {}
                    )(remote)
                    for _cls in (
                        Config,
                        Dyn,
                        Insert,
                        GEQ.make(),
                        EQ.make_sixband(cls, remote),
                        Mix,
                    )
                },
            },
        )
        return LR_cls(remote)

    @property
    def address(self) -> str:
        return f"/lr"
