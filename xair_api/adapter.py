from .bus import Bus as IBus
from .headamp import HeadAmp as IHeadAmp
from .lr import LR as ILR
from .rtn import AuxRtn as IAuxRtn
from .rtn import FxRtn as IFxRtn


class Bus(IBus):
    @property
    def address(self):
        return f'/bus/{str(self.index).zfill(2)}'


class AuxRtn(IAuxRtn):
    @property
    def address(self):
        return f'/auxin/{str(self.index).zfill(2)}'


class FxRtn(IFxRtn):
    @property
    def address(self):
        return f'/fxrtn/{str(self.index).zfill(2)}'


class MainStereo(ILR):
    @property
    def address(self) -> str:
        return '/main/st'


class MainMono(ILR):
    @property
    def address(self) -> str:
        return '/main/m'


class Matrix(ILR):
    @property
    def address(self) -> str:
        return f'/mtx/{str(self.index).zfill(2)}'


class HeadAmp(IHeadAmp):
    @property
    def address(self):
        return f'/headamp/{str(self.index).zfill(3)}'
