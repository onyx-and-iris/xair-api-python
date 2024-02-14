from typing import Optional, Union

from . import util
from .errors import XAirRemoteError
from .meta import geq_prop

"""
Classes shared by /ch, /rtn, /rtn/aux, /bus, /fxsend, /lr
"""


class Config:
    @property
    def address(self) -> str:
        root = super(Config, self).address
        return f"{root}/config"

    @property
    def name(self) -> str:
        return self.getter("name")[0]

    @name.setter
    def name(self, val: str):
        self.setter("name", val)

    @property
    def color(self) -> int:
        return self.getter("color")[0]

    @color.setter
    def color(self, val: int):
        self.setter("color", val)

    @property
    def inputsource(self) -> int:
        return self.getter("insrc")[0]

    @inputsource.setter
    def inputsource(self, val: int):
        self.setter("insrc", val)

    @property
    def usbreturn(self) -> int:
        return self.getter("rtnsrc")[0]

    @usbreturn.setter
    def usbreturn(self, val: int):
        self.setter("rtnsrc", val)


class Preamp:
    @property
    def address(self) -> str:
        root = super(Preamp, self).address
        return f"{root}/preamp"

    @property
    def usbtrim(self) -> float:
        return round(util.lin_get(-18, 18, self.getter("rtntrim")[0]), 1)

    @usbtrim.setter
    def usbtrim(self, val: float):
        if not -18 <= val <= 18:
            raise XAirRemoteError("expected value in range -18.0 to 18.0")
        self.setter("rtntrim", util.lin_set(-18, 18, val))

    @property
    def usbinput(self) -> bool:
        return self.getter("rtnsw")[0] == 1

    @usbinput.setter
    def usbinput(self, val: bool):
        self.setter("rtnsw", 1 if val else 0)

    @property
    def invert(self) -> bool:
        return self.getter("invert")[0] == 1

    @invert.setter
    def invert(self, val: bool):
        self.setter("invert", 1 if val else 0)

    @property
    def highpasson(self) -> bool:
        return self.getter("hpon")[0] == 1

    @highpasson.setter
    def highpasson(self, val: bool):
        self.setter("hpon", 1 if val else 0)

    @property
    def highpassfilter(self) -> int:
        return int(util.log_get(20, 400, self.getter("hpf")[0]))

    @highpassfilter.setter
    def highpassfilter(self, val: int):
        if not 20 <= val <= 400:
            raise XAirRemoteError("expected value in range 20 to 400")
        self.setter("hpf", util.log_set(20, 400, val))


class Gate:
    @property
    def address(self) -> str:
        root = super(Gate, self).address
        return f"{root}/gate"

    @property
    def on(self) -> bool:
        return self.getter("on")[0] == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    def mode(self) -> str:
        opts = ("gate", "exp2", "exp3", "exp4", "duck")
        return opts[self.getter("mode")[0]]

    @mode.setter
    def mode(self, val: str):
        opts = ("gate", "exp2", "exp3", "exp4", "duck")
        if val not in opts:
            raise XAirRemoteError(f"expected one of {opts}")
        self.setter("mode", opts.index(val))

    @property
    def threshold(self) -> float:
        return round(util.lin_get(-80, 0, self.getter("thr")[0]), 1)

    @threshold.setter
    def threshold(self, val: float):
        if not -80 <= val <= 0:
            raise XAirRemoteError("expected value in range -80.0 to 0.0")
        self.setter("thr", util.lin_set(-80, 0, val))

    @property
    def range(self) -> int:
        return int(util.lin_get(3, 60, self.getter("range")[0]))

    @range.setter
    def range(self, val: int):
        if not 3 <= val <= 60:
            raise XAirRemoteError("expected value in range 3 to 60")
        self.setter("range", util.lin_set(3, 60, val))

    @property
    def attack(self) -> int:
        return int(util.lin_get(0, 120, self.getter("attack")[0]))

    @attack.setter
    def attack(self, val: int):
        if not 0 <= val <= 120:
            raise XAirRemoteError("expected value in range 0 to 120")
        self.setter("attack", util.lin_set(0, 120, val))

    @property
    def hold(self) -> Union[float, int]:
        val = util.log_get(0.02, 2000, self.getter("hold")[0])
        return round(val, 1) if val < 100 else int(val)

    @hold.setter
    def hold(self, val: float):
        if not 0.02 <= val <= 2000:
            raise XAirRemoteError("expected value in range 0.02 to 2000.0")
        self.setter("hold", util.log_set(0.02, 2000, val))

    @property
    def release(self) -> int:
        return int(util.log_get(5, 4000, self.getter("release")[0]))

    @release.setter
    def release(self, val: int):
        if not 5 <= val <= 4000:
            raise XAirRemoteError("expected value in range 5 to 4000")
        self.setter("release", util.log_set(5, 4000, val))

    @property
    def keysource(self):
        return self.getter("keysrc")[0]

    @keysource.setter
    def keysource(self, val):
        self.setter("keysrc", val)

    @property
    def filteron(self):
        return self.getter("filter/on")[0] == 1

    @filteron.setter
    def filteron(self, val: bool):
        self.setter("filter/on", 1 if val else 0)

    @property
    def filtertype(self) -> int:
        return int(self.getter("filter/type")[0])

    @filtertype.setter
    def filtertype(self, val: int):
        self.setter("filter/type", val)

    @property
    def filterfreq(self) -> Union[float, int]:
        retval = util.log_get(20, 20000, self.getter("filter/f")[0])
        return int(retval) if retval > 1000 else round(retval, 1)

    @filterfreq.setter
    def filterfreq(self, val: Union[float, int]):
        if not 20 <= val <= 20000:
            raise XAirRemoteError("expected value in range 20 to 20000")
        self.setter("filter/f", util.log_set(20, 20000, val))


class Dyn:
    @property
    def address(self) -> str:
        root = super(Dyn, self).address
        return f"{root}/dyn"

    @property
    def on(self) -> bool:
        return self.getter("on")[0] == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    def mode(self) -> str:
        opts = ("comp", "exp")
        return opts[self.getter("mode")[0]]

    @mode.setter
    def mode(self, val: str):
        opts = ("comp", "exp")
        if val not in opts:
            raise XAirRemoteError(f"expected one of {opts}")
        self.setter("mode", opts.index(val))

    @property
    def det(self) -> str:
        opts = ("peak", "rms")
        return opts[self.getter("det")[0]]

    @det.setter
    def det(self, val: str):
        opts = ("peak", "rms")
        if val not in opts:
            raise XAirRemoteError(f"expected one of {opts}")
        self.setter("det", opts.index(val))

    @property
    def env(self) -> str:
        opts = ("lin", "log")
        return opts[self.getter("env")[0]]

    @env.setter
    def env(self, val: str):
        opts = ("lin", "log")
        if val not in opts:
            raise XAirRemoteError(f"expected one of {opts}")
        self.setter("env", opts.index(val))

    @property
    def threshold(self) -> float:
        return round(util.lin_get(-60, 0, self.getter("thr")[0]), 1)

    @threshold.setter
    def threshold(self, val: float):
        if not -60 <= val <= 0:
            raise XAirRemoteError("expected value in range -60.0 to 0")
        self.setter("thr", util.lin_set(-60, 0, val))

    @property
    def ratio(self) -> Union[float, int]:
        opts = (1.1, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10, 20, 100)
        return opts[self.getter("ratio")[0]]

    @ratio.setter
    def ratio(self, val: int):
        self.setter("ratio", val)

    @property
    def knee(self) -> int:
        return int(util.lin_get(0, 5, self.getter("knee")[0]))

    @knee.setter
    def knee(self, val: int):
        if not 0 <= val <= 5:
            raise XAirRemoteError("expected value in range 0 to 5")
        self.setter("knee", util.lin_set(0, 5, val))

    @property
    def mgain(self) -> float:
        return round(util.lin_get(0, 24, self.getter("mgain")[0]), 1)

    @mgain.setter
    def mgain(self, val: float):
        if not 0 <= val <= 24:
            raise XAirRemoteError("expected value in range 0.0 to 24.0")
        self.setter("mgain", util.lin_set(0, 24, val))

    @property
    def attack(self) -> int:
        return int(util.lin_get(0, 120, self.getter("attack")[0]))

    @attack.setter
    def attack(self, val: int):
        if not 0 <= val <= 120:
            raise XAirRemoteError("expected value in range 0 to 120")
        self.setter("attack", util.lin_set(0, 120, val))

    @property
    def hold(self) -> Union[float, int]:
        val = util.log_get(0.02, 2000, self.getter("hold")[0])
        return round(val, 1) if val < 100 else int(val)

    @hold.setter
    def hold(self, val: float):
        if not 0.02 <= val <= 2000:
            raise XAirRemoteError("expected value in range 0.02 to 2000.0")
        self.setter("hold", util.log_set(0.02, 2000, val))

    @property
    def release(self) -> int:
        return int(util.log_get(5, 4000, self.getter("release")[0]))

    @release.setter
    def release(self, val: int):
        if not 5 <= val <= 4000:
            raise XAirRemoteError("expected value in range 5 to 4000")
        self.setter("release", util.log_set(5, 4000, val))

    @property
    def mix(self) -> int:
        return int(util.lin_get(0, 100, self.getter("mix")[0]))

    @mix.setter
    def mix(self, val: int):
        if not 0 <= val <= 100:
            raise XAirRemoteError("expected value in range 0 to 100")
        self.setter("mix", util.lin_set(0, 100, val))

    @property
    def keysource(self):
        return self.getter("keysrc")[0]

    @keysource.setter
    def keysource(self, val):
        self.setter("keysrc", val)

    @property
    def auto(self) -> bool:
        return self.getter("auto")[0] == 1

    @auto.setter
    def auto(self, val: bool):
        self.setter("auto", 1 if val else 0)

    @property
    def filteron(self):
        return self.getter("filter/on")[0] == 1

    @filteron.setter
    def filteron(self, val: bool):
        self.setter("filter/on", 1 if val else 0)

    @property
    def filtertype(self) -> int:
        return int(self.getter("filter/type")[0])

    @filtertype.setter
    def filtertype(self, val: int):
        self.setter("filter/type", val)

    @property
    def filterfreq(self) -> Union[float, int]:
        retval = util.log_get(20, 20000, self.getter("filter/f")[0])
        return int(retval) if retval > 1000 else round(retval, 1)

    @filterfreq.setter
    def filterfreq(self, val: Union[float, int]):
        if not 20 <= val <= 20000:
            raise XAirRemoteError("expected value in range 20 to 20000")
        self.setter("filter/f", util.log_set(20, 20000, val))


class Insert:
    @property
    def address(self) -> str:
        root = super(Insert, self).address
        return f"{root}/insert"

    @property
    def on(self) -> bool:
        return self.getter("on")[0] == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    def sel(self) -> int:
        return self.getter("sel")[0]

    @sel.setter
    def sel(self, val: int):
        self.setter("sel", val)


class EQ:
    @classmethod
    def make_fourband(cls, _cls, remote, index=None):
        EQBand_cls = type("EQBand", (EQ.EQBand, _cls), {})
        return type(
            "EQ",
            (cls,),
            {
                "low": EQBand_cls(1, remote, index),
                "lomid": EQBand_cls(2, remote, index),
                "himid": EQBand_cls(3, remote, index),
                "high": EQBand_cls(4, remote, index),
            },
        )

    @classmethod
    def make_sixband(cls, _cls, remote, index=None):
        EQBand_cls = type("EQBand", (EQ.EQBand, _cls), {})
        return type(
            "EQ",
            (cls,),
            {
                "low": EQBand_cls(1, remote, index),
                "low2": EQBand_cls(2, remote, index),
                "lomid": EQBand_cls(3, remote, index),
                "himid": EQBand_cls(4, remote, index),
                "high2": EQBand_cls(5, remote, index),
                "high": EQBand_cls(6, remote, index),
            },
        )

    @property
    def address(self) -> str:
        root = super(EQ, self).address
        return f"{root}/eq"

    @property
    def on(self) -> bool:
        return self.getter("on")[0] == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    def mode(self) -> str:
        opts = ("peq", "geq", "teq")
        return opts[self.getter("mode")[0]]

    @mode.setter
    def mode(self, val: str):
        opts = ("peq", "geq", "teq")
        if val not in opts:
            raise XAirRemoteError(f"expected one of {opts}")
        self.setter("mode", opts.index(val))

    class EQBand:
        def __init__(self, i, remote, index):
            super(EQ.EQBand, self).__init__(remote, index)
            self.i = i

        @property
        def address(self) -> str:
            root = super(EQ.EQBand, self).address
            return f"{root}/eq/{self.i}"

        @property
        def type(self) -> int:
            return int(self.getter("type")[0])

        @type.setter
        def type(self, val: int):
            self.setter("type", val)

        @property
        def frequency(self) -> float:
            retval = util.log_get(20, 20000, self.getter("f")[0])
            return round(retval, 1)

        @frequency.setter
        def frequency(self, val: float):
            if not 20 <= val <= 20000:
                raise XAirRemoteError("expected value in range 20.0 to 20000.0")
            self.setter("f", util.log_set(20, 20000, val))

        @property
        def gain(self) -> float:
            return round(util.lin_get(-15, 15, self.getter("g")[0]), 1)

        @gain.setter
        def gain(self, val: float):
            if not -15 <= val <= 15:
                raise XAirRemoteError("expected value in range -15.0 to 15.0")
            self.setter("g", util.lin_set(-15, 15, val))

        @property
        def quality(self) -> float:
            retval = util.log_get(0.3, 10, self.getter("q")[0])
            return round(retval, 1)

        @quality.setter
        def quality(self, val: float):
            if not 0.3 <= val <= 10:
                raise XAirRemoteError("expected value in range 0.3 to 10.0")
            self.setter("q", util.log_set(0.3, 10, val))


class GEQ:
    @classmethod
    def make(cls):
        # fmt: off
        return type(
            "GEQ",
            (cls,),
            {
                **{
                    f"slider_{param}": geq_prop(param)
                    for param in [
                        "20", "25", "31_5", "40", "50", "63", "80", "100", "125",
                        "160", "200", "250", "315", "400", "500", "630", "800", "1k",
                        "1k25", "1k6", "2k", "2k5", "3k15", "4k", "5k", "6k3", "8k",
                        "10k", "12k5", "16k", "20k",
                    ]
                }
            },
        )
        # fmt: on

    @property
    def address(self) -> str:
        root = super(GEQ, self).address
        return f"{root}/geq"


class Mix:
    @property
    def address(self) -> str:
        root = super(Mix, self).address
        return f"{root}/mix"

    @property
    def on(self) -> bool:
        return self.getter("on")[0] == 1

    @on.setter
    def on(self, val: bool):
        self.setter("on", 1 if val else 0)

    @property
    @util.db_from
    def fader(self) -> float:
        return self.getter("fader")[0]

    @fader.setter
    @util.db_to
    def fader(self, val: float):
        self.setter("fader", val)

    @property
    def lr(self) -> bool:
        return self.getter("lr")[0] == 1

    @lr.setter
    def lr(self, val: bool):
        self.setter("lr", 1 if val else 0)


class Group:
    @property
    def address(self) -> str:
        root = super(Group, self).address
        return f"{root}/grp"

    @property
    def dca(self) -> int:
        return self.getter("dca")[0]

    @dca.setter
    def dca(self, val: int):
        self.setter("dca", val)

    @property
    def mute(self) -> int:
        return self.getter("mute")[0]

    @mute.setter
    def mute(self, val: int):
        self.setter("mute", val)


class Automix:
    @property
    def address(self) -> str:
        root = super(Automix, self).address
        return f"{root}/automix"

    @property
    def group(self) -> int:
        return self.getter("group")[0]

    @group.setter
    def group(self, val: int):
        self.setter("group", val)

    @property
    def weight(self) -> float:
        return round(util.lin_get(-12, 12, self.getter("weight")[0]), 1)

    @weight.setter
    def weight(self, val: float):
        if not -12 <= val <= 12:
            raise XAirRemoteError("expected value in range -12.0 to 12.0")
        self.setter("weight", util.lin_set(-12, 12, val))


class Send:
    def __init__(self, i, remote, index: Optional[int] = None):
        super(Send, self).__init__(remote, index)
        self.i = i + 1

    @classmethod
    def make(cls, _cls, i, remote, index=None):
        SEND_cls = type("Send", (cls, _cls), {})
        return SEND_cls(i, remote, index)

    @property
    def address(self) -> str:
        root = super(Send, self).address
        return f"{root}/mix/{str(self.i).zfill(2)}"

    @property
    @util.db_from
    def level(self) -> float:
        return self.getter("level")[0]

    @level.setter
    @util.db_to
    def level(self, val: float):
        self.setter("level", val)
