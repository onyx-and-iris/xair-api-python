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


class TestSetAndGetAuxInConfigHigher:
    """Config"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "auxin")
        self.target = getattr(self.target[data.auxrtn], "config")

    @pytest.mark.parametrize(
        "param,value",
        [("name", "test0"), ("name", "test1")],
    )
    def test_it_sets_and_gets_auxrtn_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" FX RETURN TESTS """


class TestSetAndGetFXReturnConfigHigher:
    """Config"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "fxreturn")
        self.target = getattr(self.target[data.fx], "config")

    @pytest.mark.parametrize(
        "param,value",
        [("name", "test0"), ("name", "test1")],
    )
    def test_it_sets_and_gets_fxrtn_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value


""" MATRIX TESTS """


class TestSetAndGetMatrixConfigHigher:
    """Config"""

    __test__ = True

    def setup_class(self):
        self.target = getattr(tests, "matrix")
        self.target = getattr(self.target[data.matrix], "config")

    @pytest.mark.parametrize(
        "param,value",
        [("name", "test0"), ("name", "test1")],
    )
    def test_it_sets_and_gets_matrix_string_params(self, param, value):
        setattr(self.target, param, value)
        assert getattr(self.target, param) == value
