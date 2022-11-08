import pytest

from tests.x32 import data, tests

""" STRIP TESTS """


class TestSetAndGetStripMixHigher:
    """Mix"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "strip")
        self.target = getattr(self.target[data.strip], "mix")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False)],
    )
    def test_it_sets_and_gets_strip_bool_params(self, param, value):
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
    def test_it_sets_and_gets_bus_int_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" AUXIN TESTS """


class TestSetAndGetAuxInPreampHigher:
    """Preamp"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "auxin")
        self.target = getattr(self.target[data.auxrtn], "preamp")

    @pytest.mark.parametrize(
        "param,value",
        [("invert", True), ("invert", False)],
    )
    def test_it_sets_and_gets_auxrtn_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" FX RETURN TESTS """


class TestSetAndGetFXReturnEQHigher:
    """EQ"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "fxreturn")
        self.target = getattr(self.target[data.fx], "eq")

    @pytest.mark.parametrize(
        "param,value",
        [("on", True), ("on", False)],
    )
    def test_it_sets_and_gets_fxrtn_bool_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" MATRIX TESTS """


class TestSetAndGetMatrixDynHigher:
    """Dyn"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "matrix")
        self.target = getattr(self.target[data.matrix], "dyn")

    @pytest.mark.parametrize(
        "param,value",
        [("mode", "comp"), ("mode", "exp")],
    )
    def test_it_sets_and_gets_matrix_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" MAIN STEREO TESTS """


class TestSetAndGetMainStereoInsertHigher:
    """Insert"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "mainst")

    @pytest.mark.parametrize(
        "param,value",
        [("mode", "comp"), ("mode", "exp")],
    )
    def test_it_sets_and_gets_mainst_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value
