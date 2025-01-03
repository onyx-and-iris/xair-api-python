import abc
import logging

from . import util

logger = logging.getLogger(__name__)


class IHeadAmp(abc.ABC):
    """Abstract Base Class for headamps"""

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


class HeadAmp(IHeadAmp):
    """Concrete class for headamps"""

    @property
    def address(self):
        return f"/headamp/{str(self.index).zfill(2)}"

    @property
    def gain(self):
        return round(util.lin_get(-12, 60, self.getter("gain")[0]), 1)

    @gain.setter
    def gain(self, val):
        self.setter("gain", util.lin_set(-12, 60, val))

    @property
    def phantom(self):
        return self.getter("phantom")[0] == 1

    @phantom.setter
    def phantom(self, val):
        self.setter("phantom", 1 if val else 0)
