from typing import Union

from .errors import MAirRemoteError
from .util import lin_get, lin_set, log_get, log_set, _get_fader_val, _set_fader_val
from .meta import geq_prop

"""
Classes shared by /ch, /rtn, /rt/aux, /bus, /fxsend, /lr
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
        if not isinstance(val, str):
            raise MAirRemoteError("name is a string parameter")
        self.setter("name", val)

    @property
    def color(self) -> int:
        return self.getter("color")[0]

    @color.setter
    def color(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("color is an int parameter")
        self.setter("color", val)

    @property
    def inputsource(self) -> int:
        return self.getter("insrc")[0]

    @inputsource.setter
    def inputsource(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("inputsource is an int parameter")
        self.setter("insrc", val)

    @property
    def usbreturn(self) -> int:
        return self.getter("rtnsrc")[0]

    @usbreturn.setter
    def usbreturn(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("usbreturn is an int parameter")
        self.setter("rtnsrc", val)


class Preamp:
    @property
    def address(self) -> str:
        root = super(Preamp, self).address
        return f"{root}/preamp"

    @property
    def usbtrim(self) -> float:
        return round(lin_get(-18, 18, self.getter("rtntrim")[0]), 1)

    @usbtrim.setter
    def usbtrim(self, val: float):
        if not isinstance(val, float):
            raise MAirRemoteError(
                "usbtrim is a float parameter, expected value in range -18 to 18"
            )
        self.setter("rtntrim", lin_set(-18, 18, val))

    @property
    def usbinput(self) -> bool:
        return self.getter("rtnsw")[0] == 1

    @usbinput.setter
    def usbinput(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("rtnsw is a bool parameter")
        self.setter("rtnsw", 1 if val else 0)

    @property
    def invert(self) -> bool:
        return self.getter("invert")[0] == 1

    @invert.setter
    def invert(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("invert is a bool parameter")
        self.setter("invert", 1 if val else 0)

    @property
    def highpasson(self) -> bool:
        return self.getter("hpon")[0] == 1

    @highpasson.setter
    def highpasson(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("hpon is a bool parameter")
        self.setter("hpon", 1 if val else 0)

    @property
    def highpassfilter(self) -> int:
        return int(log_get(20, 400, self.getter("hpf")[0]))

    @highpassfilter.setter
    def highpassfilter(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("highpassfilter is an int parameter")
        self.setter("hpf", log_set(20, 400, val))


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
        if not isinstance(val, bool):
            raise MAirRemoteError("on is a boolean parameter")
        self.setter("on", 1 if val else 0)

    @property
    def mode(self) -> str:
        opts = ("gate", "exp2", "exp3", "exp4", "duck")
        return opts[self.getter("mode")[0]]

    @mode.setter
    def mode(self, val: str):
        opts = ("gate", "exp2", "exp3", "exp4", "duck")
        if not isinstance(val, str) and val not in opts:
            raise MAirRemoteError(f"mode is a string parameter, expected one of {opts}")
        self.setter("mode", opts.index(val))

    @property
    def threshold(self) -> float:
        return round(lin_get(-80, 0, self.getter("thr")[0]), 1)

    @threshold.setter
    def threshold(self, val: float):
        if not isinstance(val, float):
            raise MAirRemoteError(
                "threshold is a float parameter, expected value in range -80 to 0"
            )
        self.setter("thr", lin_set(-80, 0, val))

    @property
    def range(self) -> int:
        return int(lin_get(3, 60, self.getter("range")[0]))

    @range.setter
    def range(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError(
                "range is an int parameter, expected value in range 3 to 60"
            )
        self.setter("range", lin_set(3, 60, val))

    @property
    def attack(self) -> int:
        return int(lin_get(0, 120, self.getter("attack")[0]))

    @attack.setter
    def attack(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError(
                "attack is an int parameter, expected value in range 0 to 120"
            )
        self.setter("attack", lin_set(0, 120, val))

    @property
    def hold(self) -> Union[float, int]:
        val = log_get(0.02, 2000, self.getter("hold")[0])
        return round(val, 1) if val < 100 else int(val)

    @hold.setter
    def hold(self, val: float):
        self.setter("hold", log_set(0.02, 2000, val))

    @property
    def release(self) -> int:
        return int(log_get(5, 4000, self.getter("release")[0]))

    @release.setter
    def release(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError(
                "release is an int parameter, expected value in range 5 to 4000"
            )
        self.setter("release", log_set(5, 4000, val))

    @property
    def keysource(self):
        return self.getter("keysrc")[0]

    @keysource.setter
    def keysource(self, val):
        if not isinstance(val, int):
            raise MAirRemoteError("keysource is an int parameter")
        self.setter("keysrc", val)

    @property
    def filteron(self):
        return self.getter("filter/on")[0] == 1

    @filteron.setter
    def filteron(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("filteron is a boolean parameter")
        self.setter("filter/on", 1 if val else 0)

    @property
    def filtertype(self) -> int:
        return int(self.getter("filter/type")[0])

    @filtertype.setter
    def filtertype(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("filtertype is an int parameter")
        self.setter("filter/type", val)

    @property
    def filterfreq(self) -> Union[float, int]:
        retval = log_get(20, 20000, self.getter("filter/f")[0])
        return int(retval) if retval > 1000 else round(retval, 1)

    @filterfreq.setter
    def filterfreq(self, val: Union[float, int]):
        self.setter("filter/f", log_set(20, 20000, val))


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
        if not isinstance(val, bool):
            raise MAirRemoteError("on is a boolean parameter")
        self.setter("on", 1 if val else 0)

    @property
    def mode(self) -> str:
        opts = ("comp", "exp")
        return opts[self.getter("mode")[0]]

    @mode.setter
    def mode(self, val: str):
        opts = ("comp", "exp")
        if not isinstance(val, str) and val not in opts:
            raise MAirRemoteError(f"mode is a string parameter, expected one of {opts}")
        self.setter("mode", opts.index(val))

    @property
    def det(self) -> str:
        opts = ("peak", "rms")
        return opts[self.getter("det")[0]]

    @det.setter
    def det(self, val: str):
        opts = ("peak", "rms")
        if not isinstance(val, str) and val not in opts:
            raise MAirRemoteError(f"det is a string parameter, expected one of {opts}")
        self.setter("det", opts.index(val))

    @property
    def env(self) -> str:
        opts = ("lin", "log")
        return opts[self.getter("env")[0]]

    @env.setter
    def env(self, val: str):
        opts = ("lin", "log")
        if not isinstance(val, str) and val not in opts:
            raise MAirRemoteError(f"env is a string parameter, expected one of {opts}")
        self.setter("env", opts.index(val))

    @property
    def threshold(self) -> float:
        return round(lin_get(-60, 0, self.getter("thr")[0]), 1)

    @threshold.setter
    def threshold(self, val: float):
        if not isinstance(val, float):
            raise MAirRemoteError(
                "threshold is a float parameter, expected value in range -80 to 0"
            )
        self.setter("thr", lin_set(-60, 0, val))

    @property
    def ratio(self) -> Union[float, int]:
        opts = (1.1, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10, 20, 100)
        return opts[self.getter("ratio")[0]]

    @ratio.setter
    def ratio(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("ratio is an int parameter")
        self.setter("ratio", val)

    @property
    def knee(self) -> int:
        return int(lin_get(0, 5, self.getter("knee")[0]))

    @knee.setter
    def knee(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError(
                "knee is an int parameter, expected value in range 0 to 5"
            )
        self.setter("knee", lin_set(0, 5, val))

    @property
    def mgain(self) -> float:
        return round(lin_get(0, 24, self.getter("mgain")[0]), 1)

    @mgain.setter
    def mgain(self, val: float):
        self.setter("mgain", lin_set(0, 24, val))

    @property
    def attack(self) -> int:
        return int(lin_get(0, 120, self.getter("attack")[0]))

    @attack.setter
    def attack(self, val: int):
        self.setter("attack", lin_set(0, 120, val))

    @property
    def hold(self) -> Union[float, int]:
        val = log_get(0.02, 2000, self.getter("hold")[0])
        return round(val, 1) if val < 100 else int(val)

    @hold.setter
    def hold(self, val: float):
        self.setter("hold", log_set(0.02, 2000, val))

    @property
    def release(self) -> int:
        return int(log_get(5, 4000, self.getter("release")[0]))

    @release.setter
    def release(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError(
                "release is an int parameter, expected value in range 5 to 4000"
            )
        self.setter("release", log_set(5, 4000, val))

    @property
    def mix(self) -> int:
        return int(lin_get(0, 100, self.getter("mix")[0]))

    @mix.setter
    def mix(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError(
                "mix is an int parameter, expected value in range 0 to 5"
            )
        self.setter("mix", lin_set(0, 100, val))

    @property
    def keysource(self):
        return self.getter("keysrc")[0]

    @keysource.setter
    def keysource(self, val):
        if not isinstance(val, int):
            raise MAirRemoteError("keysource is an int parameter")
        self.setter("keysrc", val)

    @property
    def auto(self) -> bool:
        return self.getter("auto")[0] == 1

    @auto.setter
    def auto(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("auto is a boolean parameter")
        self.setter("auto", 1 if val else 0)

    @property
    def filteron(self):
        return self.getter("filter/on")[0] == 1

    @filteron.setter
    def filteron(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("filteron is a boolean parameter")
        self.setter("filter/on", 1 if val else 0)

    @property
    def filtertype(self) -> int:
        return int(self.getter("filter/type")[0])

    @filtertype.setter
    def filtertype(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("filtertype is an int parameter")
        self.setter("filter/type", val)

    @property
    def filterfreq(self) -> Union[float, int]:
        retval = log_get(20, 20000, self.getter("filter/f")[0])
        return int(retval) if retval > 1000 else round(retval, 1)

    @filterfreq.setter
    def filterfreq(self, val: Union[float, int]):
        self.setter("filter/f", log_set(20, 20000, val))


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
        if not isinstance(val, bool):
            raise MAirRemoteError("on is a boolean parameter")
        self.setter("on", 1 if val else 0)

    @property
    def sel(self) -> int:
        return self.getter("sel")[0]

    @sel.setter
    def sel(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("sel is an int parameter")
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
        if not isinstance(val, bool):
            raise MAirRemoteError("on is a boolean parameter")
        self.setter("on", 1 if val else 0)

    @property
    def mode(self) -> str:
        opts = ("peq", "geq", "teq")
        return opts[self.getter("mode")[0]]

    @mode.setter
    def mode(self, val: str):
        opts = ("peq", "geq", "teq")
        if not isinstance(val, str) and val not in opts:
            raise MAirRemoteError(f"mode is a string parameter, expected one of {opts}")
        self.setter("mode", opts.index(val))

    class EQBand:
        def __init__(self, i, remote, index):
            if index is None:
                super(EQ.EQBand, self).__init__(remote)
            else:
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
            if not isinstance(val, int):
                raise MAirRemoteError("type is an int parameter")
            self.setter(f"type", val)

        @property
        def frequency(self) -> float:
            retval = log_get(20, 20000, self.getter("f")[0])
            return round(retval, 1)

        @frequency.setter
        def frequency(self, val: float):
            self.setter("f", log_set(20, 20000, val))

        @property
        def gain(self) -> float:
            return round(lin_get(-15, 15, self.getter("g")[0]), 1)

        @gain.setter
        def gain(self, val: float):
            self.setter("g", lin_set(-15, 15, val))

        @property
        def quality(self) -> float:
            retval = log_get(0.3, 10, self.getter("q")[0])
            return round(retval, 1)

        @quality.setter
        def quality(self, val: float):
            self.setter("q", log_set(0.3, 10, val))


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
                        "160", "200", "250", "315" "400", "500", "630", "800", "1k",
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
        if not isinstance(val, bool):
            raise MAirRemoteError("on is a boolean parameter")
        self.setter("on", 1 if val else 0)

    @property
    def fader(self) -> float:
        retval = self.getter("fader")[0]
        return _get_fader_val(retval)

    @fader.setter
    def fader(self, val: float):
        _set_fader_val(self, val)

    @property
    def lr(self) -> bool:
        return self.getter("lr")[0] == 1

    @lr.setter
    def lr(self, val: bool):
        if not isinstance(val, bool):
            raise MAirRemoteError("lr is a boolean parameter")
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
        if not isinstance(val, int):
            raise MAirRemoteError("dca is an int parameter")
        self.setter("dca", val)

    @property
    def mute(self) -> int:
        return self.getter("mute")[0]

    @mute.setter
    def mute(self, val: int):
        if not isinstance(val, int):
            raise MAirRemoteError("mute is an int parameter")
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
        if not isinstance(val, int):
            raise MAirRemoteError("group is an int parameter")
        self.setter("group", val)

    @property
    def weight(self) -> float:
        return round(lin_get(-12, 12, self.getter("weight")[0]), 1)

    @weight.setter
    def weight(self, val: float):
        if not isinstance(val, float):
            raise MAirRemoteError(
                "weight is a float parameter, expected value in range -12 to 12"
            )
        self.setter("weight", lin_set(-12, 12, val))
