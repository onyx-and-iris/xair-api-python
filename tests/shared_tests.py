from nose.tools import assert_equal, nottest
from parameterized import parameterized, parameterized_class

import unittest
from tests import tests

"""
Not every subclass is tested for every superclass to avoid redundancy.
LR:     mix, config, insert, geq
Strip:  mix, preamp, config, gate, automix
Bus:    config, dyn, eq
FXSend: group
"""

""" LR TESTS """
#@nottest
class TestSetAndGetLRMixHigher(unittest.TestCase):   
    """ Mix """
    def setUp(self):
        self.target = getattr(tests, 'lr')
        self.target = getattr(self.target, 'mix')

    @parameterized.expand([
    ('on', True), ('on', False)
    ])
    def test_it_sets_and_gets_lr_bool_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

    @parameterized.expand([
    ('fader', -80.6), ('fader', -67.0)
    ])
    def test_it_sets_and_gets_lr_float_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
class TestSetAndGetLRConfigHigher(unittest.TestCase):
    """ Config """
    def setUp(self):
        self.target = getattr(tests, 'lr')
        self.target = getattr(self.target, 'config')

    @parameterized.expand([
    ('name', 'test0'), ('name', 'test1')
    ])
    def test_it_sets_and_gets_lr_string_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
class TestSetAndGetLRInsertHigher(unittest.TestCase):   
    """ Insert """
    def setUp(self):
        self.target = getattr(tests, 'lr')
        self.target = getattr(self.target, 'insert')

    @parameterized.expand([
    ('on', True), ('on', False)
    ])
    def test_it_sets_and_gets_lr_bool_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

    @parameterized.expand([
    ('sel', 0), ('sel', 4)
    ])
    def test_it_sets_and_gets_lr_int_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
class TestSetAndGetLRGEQHigher(unittest.TestCase):   
    """ GEQ """
    def setUp(self):
        self.target = getattr(tests, 'lr')
        self.target = getattr(self.target, 'geq')

    @parameterized.expand([
    ('slider_20', -13.5), ('slider_20', 5.5), ('slider_6k3', -8.5), ('slider_6k3', 8.5)
    ])
    def test_it_sets_and_gets_lr_int_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)


""" STRIP TESTS """
#@nottest
@parameterized_class([
    { 'i': 15 }
])
class TestSetAndGetStripMixHigher(unittest.TestCase):
    """ Mix """
    def setUp(self):
        self.target = getattr(tests, 'strip')
        self.target = getattr(self.target[self.i], 'mix')

    @parameterized.expand([
    ('on', True), ('on', False), ('lr', True), ('lr', False)
    ])
    def test_it_sets_and_gets_strip_bool_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

#@nottest
@parameterized_class([
    { 'i': 8 }
])
class TestSetAndGetStripPreampHigher(unittest.TestCase):
    """ Preamp """
    def setUp(self):
        self.target = getattr(tests, 'strip')
        self.target = getattr(self.target[self.i], 'preamp')

    @parameterized.expand([
    ('highpasson', True), ('highpasson', False), ('usbinput', True), ('usbinput', False)
    ])
    def test_it_sets_and_gets_strip_bool_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

    @parameterized.expand([
    ('highpassfilter', 20), ('highpassfilter', 399)
    ])
    def test_it_sets_and_gets_strip_int_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

    @parameterized.expand([
    ('usbtrim', -16.5), ('usbtrim', 5.5)
    ])
    def test_it_sets_and_gets_strip_float_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
@parameterized_class([
    { 'i': 3 }
])
class TestSetAndGetStripConfigHigher(unittest.TestCase):
    """ Config """
    def setUp(self):
        self.target = getattr(tests, 'strip')
        self.target = getattr(self.target[self.i], 'config')

    @parameterized.expand([
    ('inputsource', 0), ('inputsource', 18), ('usbreturn', 3), ('usbreturn', 12)
    ])
    def test_it_sets_and_gets_strip_int_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

@parameterized_class([
    { 'i': 12 }
])
class TestSetAndGetStripGateHigher(unittest.TestCase):
    """ Gate """
    def setUp(self):
        self.target = getattr(tests, 'strip')
        self.target = getattr(self.target[self.i], 'gate')

    @parameterized.expand([
    ('on', True), ('on', False), ('invert', True), ('invert', False),
    ('filteron', True), ('filteron', False)
    ])
    def test_it_sets_and_gets_strip_bool_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

    @parameterized.expand([
    ('range', 11), ('range', 48), ('attack', 5), ('attack', 110),
    ('release', 360), ('release', 2505), ('filtertype', 0), ('filtertype', 8)
    ])
    def test_it_sets_and_gets_strip_int_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

    @parameterized.expand([
    ('mode', 'exp2'), ('mode', 'duck')
    ])
    def test_it_sets_and_gets_strip_string_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

    @parameterized.expand([
    ('threshold', -80.0), ('threshold', 0.0), ('hold', 355), ('hold', 63.2),
    ('filterfreq', 37.2), ('filterfreq', 12765)
    ])
    def test_it_sets_and_gets_strip_float_params(self, param, val):
        setattr(self.target,  param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
@parameterized_class([
    { 'i': 6 }
])
class TestSetAndGetStripAutomixHigher(unittest.TestCase):
    """ Automix """
    def setUp(self):
        self.target = getattr(tests, 'strip')
        self.target = getattr(self.target[self.i], 'automix')

    @parameterized.expand([
    ('group', 0), ('group', 2)
    ])
    def test_it_sets_and_gets_fxsend_int_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

    @parameterized.expand([
    ('weight', -10.5), ('weight', 3.5)
    ])
    def test_it_sets_and_gets_fxsend_float_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)


""" BUS TESTS """
#@nottest
@parameterized_class([
    { 'i': 1 }
])
class TestSetAndGetBusConfigHigher(unittest.TestCase):
    """ Config """
    def setUp(self):
        self.target = getattr(tests, 'bus')
        self.target = getattr(self.target[self.i], 'config')

    @parameterized.expand([
    ('color', 0), ('color', 15)
    ])
    def test_it_sets_and_gets_bus_bool_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
@parameterized_class([
    { 'i': 2 }
])
class TestSetAndGetBusDynHigher(unittest.TestCase):
    """ Dyn """
    def setUp(self):
        self.target = getattr(tests, 'bus')
        self.target = getattr(self.target[self.i], 'dyn')

    @parameterized.expand([
    ('on', True), ('on', False)
    ])
    def test_it_sets_and_gets_bus_bool_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

    @parameterized.expand([
    ('mode', 'comp'), ('mode', 'exp'), ('env', 'lin'), ('env', 'log'),
    ('det', 'peak'), ('det', 'rms')
    ])
    def test_it_sets_and_gets_bus_string_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)

#@nottest
@parameterized_class([
    { 'i': 0 }
])
class TestSetAndGetBusEQHigher(unittest.TestCase):
    """ EQ """
    def setUp(self):
        self.target = getattr(tests, 'bus')
        self.target = getattr(self.target[self.i], 'eq')

    @parameterized.expand([
    ('on', True), ('on', False)
    ])
    def test_it_sets_and_gets_bus_bool_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        self.assertTrue(isinstance(retval, bool))
        assert_equal(retval, val)

    @parameterized.expand([
    ('mode', 'peq'), ('mode', 'geq'), ('mode', 'teq')
    ])
    def test_it_sets_and_gets_bus_string_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)


""" FXSEND TESTS """
#@nottest
@parameterized_class([
    { 'i': 1 }
])
class TestSetAndGetFXSendGroupHigher(unittest.TestCase):
    """ Group """
    def setUp(self):
        self.target = getattr(tests, 'fxsend')
        self.target = getattr(self.target[self.i], 'group')

    @parameterized.expand([
    ('dca', 0), ('dca', 12), ('mute', 3), ('mute', 8)
    ])
    def test_it_sets_and_gets_fxsend_int_params(self, param, val):
        setattr(self.target, param, val)
        retval = getattr(self.target, param)
        assert_equal(retval, val)
