import abc
import logging

from . import kinds, util
from .meta import bool_prop

logger = logging.getLogger(__name__)


class IConfig(abc.ABC):
    """Abstract Base Class for config"""

    def __init__(self, remote):
        self._remote = remote
        self.logger = logger.getChild(self.__class__.__name__)

    def getter(self, param: str):
        return self._remote.query(f"{self.address}/{param}")

    def setter(self, param: str, val: int):
        self._remote.send(f"{self.address}/{param}", val)

    @abc.abstractmethod
    def address(self):
        pass


class Config(IConfig):
    """Concrete class for config"""

    @classmethod
    def make(cls, remote):
        """
        Factory function for Config

        Returns a Config class of a kind.
        """
        LINKS_cls = _make_links_mixins[remote.kind.id_]
        MUTEGROUP_cls = type("MuteGroup", (Config.MuteGroup, cls), {})
        MONITOR_cls = type("ConfigMonitor", (Config.Monitor, cls), {})
        CONFIG_cls = type(
            f"Config{remote.kind}",
            (cls, LINKS_cls),
            {
                "mute_group": tuple(MUTEGROUP_cls(remote, i) for i in range(4)),
                "monitor": MONITOR_cls(remote),
            },
        )
        return CONFIG_cls(remote)

    @property
    def address(self) -> str:
        return "/config"

    @property
    def amixenable(self) -> bool:
        return self.getter("mute")[0] == 1

    @amixenable.setter
    def amixenable(self, val: bool):
        self.setter("amixenable", 1 if val else 0)

    @property
    def amixlock(self) -> bool:
        return self.getter("amixlock")[0] == 1

    @amixlock.setter
    def amixlock(self, val: bool):
        self.setter("amixlock", 1 if val else 0)

    class MuteGroup:
        def __init__(self, remote, i):
            super(Config.MuteGroup, self).__init__(remote)
            self.i = i + 1

        @property
        def address(self) -> str:
            root = super(Config.MuteGroup, self).address
            return f"{root}/mute"

        @property
        def on(self) -> bool:
            return self.getter(f"{self.i}")[0] == 1

        @on.setter
        def on(self, val: bool):
            self.setter(f"{self.i}", 1 if val else 0)

    class Monitor:
        @property
        def address(self) -> str:
            root = super(Config.Monitor, self).address
            return f"{root}/solo"

        @property
        @util.db_from
        def level(self) -> float:
            return self.getter("level")[0]

        @level.setter
        @util.db_to
        def level(self, val: float):
            self.setter("level", val)

        @property
        def source(self) -> int:
            return int(self.getter("source")[0])

        @source.setter
        def source(self, val: int):
            self.setter("source", val)

        @property
        def sourcetrim(self) -> float:
            return round(util.lin_get(-18, 18, self.getter("sourcetrim")[0]), 1)

        @sourcetrim.setter
        def sourcetrim(self, val: float):
            if not -18 <= val <= 18:
                self.logger.warning(
                    f"sourcetrim got {val}, expected value in range -18.0 to 18.0"
                )
            self.setter("sourcetrim", util.lin_set(-18, 18, val))

        @property
        def chmode(self) -> bool:
            return self.getter("chmode")[0] == 1

        @chmode.setter
        def chmode(self, val: bool):
            self.setter("chmode", 1 if val else 0)

        @property
        def busmode(self) -> bool:
            return self.getter("busmode")[0] == 1

        @busmode.setter
        def busmode(self, val: bool):
            self.setter("busmode", 1 if val else 0)

        @property
        def dimgain(self) -> int:
            return int(util.lin_get(-40, 0, self.getter("dimatt")[0]))

        @dimgain.setter
        def dimgain(self, val: int):
            if not -40 <= val <= 0:
                self.logger.warning(
                    f"dimgain got {val}, expected value in range -40 to 0"
                )
            self.setter("dimatt", util.lin_set(-40, 0, val))

        @property
        def dim(self) -> bool:
            return self.getter("dim")[0] == 1

        @dim.setter
        def dim(self, val: bool):
            self.setter("dim", 1 if val else 0)

        @property
        def mono(self) -> bool:
            return self.getter("mono")[0] == 1

        @mono.setter
        def mono(self, val: bool):
            self.setter("mono", 1 if val else 0)

        @property
        def mute(self) -> bool:
            return self.getter("mute")[0] == 1

        @mute.setter
        def mute(self, val: bool):
            self.setter("mute", 1 if val else 0)

        @property
        def dimfpl(self) -> bool:
            return self.getter("dimfpl")[0] == 1

        @dimfpl.setter
        def dimfpl(self, val: bool):
            self.setter("dimfpl", 1 if val else 0)


def _make_links_mixin(kind):
    """Creates a links mixin"""
    return type(
        f"Links{kind}",
        (),
        {
            "link_eq": bool_prop("linkcfg/eq"),
            "link_dyn": bool_prop("linkcfg/dyn"),
            "link_fader_mute": bool_prop("linkcfg/fdrmute"),
            **{
                f"chlink{i}_{i+1}": bool_prop(f"chlink/{i}-{i+1}")
                for i in range(1, kind.num_strip, 2)
            },
            **{
                f"buslink{i}_{i+1}": bool_prop(f"buslink/{i}-{i+1}")
                for i in range(1, kind.num_bus, 2)
            },
        },
    )


_make_links_mixins = {kind.id_: _make_links_mixin(kind) for kind in kinds.all}
