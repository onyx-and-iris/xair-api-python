import pytest

from tests.xair import data, tests

"""
Not every subclass is tested for every superclass to avoid redundancy.
LR:     mix, config, insert, geq
Strip:  mix, preamp, config, gate, automix
Bus:    config, dyn, eq
FXSend: group
"""

""" Main LR TESTS """


class TestSetAndGetLRMixHigher:
    """Mix"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "lr")
        self.target = getattr(self.target, "mix")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False)],
    )
    def test_it_sets_and_gets_lr_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("fader", -80.6), ("fader", -67.0)],
    )
    def test_it_sets_and_gets_lr_float_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetLRConfigHigher:
    """Config"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "lr")
        self.target = getattr(self.target, "config")

    @pytest.mark.parametrize("param,value", [("name", "test0"), ("name", "test1")])
    def test_it_sets_and_gets_lr_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetLRInsertHigher:
    """Insert"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "lr")
        self.target = getattr(self.target, "insert")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False)],
    )
    def test_it_sets_and_gets_lr_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("sel", 0), ("sel", 4)],
    )
    def test_it_sets_and_gets_lr_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetLRGEQHigher:
    """GEQ"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "lr")
        self.target = getattr(self.target, "geq")

    @pytest.mark.parametrize(
        "param,value",
        [
            ("slider_20", -13.5),
            ("slider_20", 5.5),
            ("slider_6k3", -8.5),
            ("slider_6k3", 8.5),
        ],
    )
    def test_it_sets_and_gets_lr_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" STRIP TESTS """


class TestSetAndGetStripMuteHigher:
    """Mute"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")[data.strip]

    @pytest.mark.parametrize(
        "param,value",
        [("mute", True), ("mute", False)],
    )
    def test_it_sets_and_gets_strip_mute_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetStripMixHigher:
    """Mix"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")
        self.target = getattr(self.target[data.strip], "mix")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False), ("lr", True), ("lr", False)],
    )
    def test_it_sets_and_gets_strip_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetStripPreampHigher:
    """Preamp"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")
        self.target = getattr(self.target[data.strip], "preamp")

    @pytest.mark.parametrize(
        "param,value",
        [
            ("highpasson", True),
            ("highpasson", False),
            ("usbinput", True),
            ("usbinput", False),
        ],
    )
    def test_it_sets_and_gets_strip_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("highpassfilter", 20), ("highpassfilter", 399)],
    )
    def test_it_sets_and_gets_strip_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("usbtrim", -16.5), ("usbtrim", 5.5)],
    )
    def test_it_sets_and_gets_strip_float_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetStripConfigHigher:
    """Config"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")
        self.target = getattr(self.target[data.strip], "config")

    @pytest.mark.parametrize(
        "param,value",
        [("inputsource", 0), ("inputsource", 18), ("usbreturn", 3), ("usbreturn", 12)],
    )
    def test_it_sets_and_gets_strip_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetStripGateHigher:
    """Gate"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")
        self.target = getattr(self.target[data.strip], "gate")

    @pytest.mark.parametrize(
        "param,value",
        [
            ("on", True),
            ("on", False),
            ("invert", True),
            ("invert", False),
            ("filteron", True),
            ("filteron", False),
        ],
    )
    def test_it_sets_and_gets_strip_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [
            ("range", 11),
            ("range", 48),
            ("attack", 5),
            ("attack", 110),
            ("release", 360),
            ("release", 2505),
            ("filtertype", 0),
            ("filtertype", 8),
        ],
    )
    def test_it_sets_and_gets_strip_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("mode", "exp2"), ("mode", "duck")],
    )
    def test_it_sets_and_gets_strip_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [
            ("threshold", -80.0),
            ("threshold", 0.0),
            ("hold", 355),
            ("hold", 63.2),
            ("filterfreq", 37.2),
            ("filterfreq", 12765),
        ],
    )
    def test_it_sets_and_gets_strip_float_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetStripAutomixHigher:
    """Automix"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")
        self.target = getattr(self.target[data.strip], "automix")

    @pytest.mark.parametrize(
        "param,value",
        [("group", 0), ("group", 2)],
    )
    def test_it_sets_and_gets_strip_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("weight", -10.5), ("weight", 3.5)],
    )
    def test_it_sets_and_gets_strip_float_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" BUS TESTS """


class TestSetAndGetBusConfigHigher:
    """Config"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "bus")
        self.target = getattr(self.target[data.bus], "config")

    @pytest.mark.parametrize(
        "param,value",
        [("color", 0), ("color", 15)],
    )
    def test_it_sets_and_gets_bus_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetBusDynHigher:
    """Dyn"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "bus")
        self.target = getattr(self.target[data.bus], "dyn")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False)],
    )
    def test_it_sets_and_gets_bus_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [
            ("mode", "comp"),
            ("mode", "exp"),
            ("env", "lin"),
            ("env", "log"),
            ("det", "peak"),
            ("det", "rms"),
        ],
    )
    def test_it_sets_and_gets_bus_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


class TestSetAndGetBusEQHigher:
    """EQ"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "bus")
        self.target = getattr(self.target[data.bus], "eq")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False)],
    )
    def test_it_sets_and_gets_bus_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value

    @pytest.mark.parametrize(
        "param,value",
        [("mode", "peq"), ("mode", "geq"), ("mode", "teq")],
    )
    def test_it_sets_and_gets_bus_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" FXSEND TESTS """


class TestSetAndGetFXSendGroupHigher:
    """Group"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "fxsend")
        self.target = getattr(self.target[data.fx], "group")

    @pytest.mark.parametrize(
        "param,value",
        [("dca", 0), ("dca", 12), ("mute", 3), ("mute", 8)],
    )
    def test_it_sets_and_gets_fxsend_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value
