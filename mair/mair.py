import abc
import time
import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.osc_message_builder import OscMessageBuilder
from configparser import ConfigParser
from pathlib import Path
from typing import Union

from . import kinds
from .lr import LR
from .strip import Strip
from .bus import Bus
from .dca import DCA
from .fx import FXSend, FXReturn
from .config import Config
from .rtn import Aux, Rtn


class OSCClientServer(BlockingOSCUDPServer):
    def __init__(self, address, dispatcher):
        super().__init__(("", 0), dispatcher)
        self.xr_address = address

    def send_message(self, address, value):
        builder = OscMessageBuilder(address=address)
        if value is None:
            values = list()
        elif isinstance(value, list):
            values = value
        else:
            values = [value]
        for val in values:
            builder.add_arg(val)
        msg = builder.build()
        self.socket.sendto(msg.dgram, self.xr_address)


class MAirRemote(abc.ABC):
    """
    Handles the communication with the M-Air mixer via the OSC protocol
    """

    _CONNECT_TIMEOUT = 0.5
    _WAIT_TIME = 0.025
    _REFRESH_TIMEOUT = 5

    XAIR_PORT = 10024

    info_response = []

    def __init__(self, **kwargs):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.msg_handler)
        self.xair_ip = kwargs["ip"] or self._ip_from_ini()
        self.xair_port = kwargs["port"] or self.XAIR_PORT
        self.server = OSCClientServer((self.xair_ip, self.xair_port), dispatcher)

    def __enter__(self):
        self.worker = threading.Thread(target=self.run_server)
        self.worker.daemon = True
        self.worker.start()
        self.validate_connection()
        return self

    def _ip_from_ini(self):
        ini_path = Path.cwd() / "config.ini"
        parser = ConfigParser()
        if not parser.read(ini_path):
            print("Could not read config file")
        return parser["connection"].get("ip")

    def validate_connection(self):
        self.send("/xinfo")
        time.sleep(self._CONNECT_TIMEOUT)
        if len(self.info_response) > 0:
            print(f"Successfully connected to {self.info_response[2]}.")
        else:
            print(
                "Error: Failed to setup OSC connection to mixer. Please check for correct ip address."
            )

    def run_server(self):
        self.server.serve_forever()

    def msg_handler(self, addr, *data):
        self.info_response = data[:]

    def send(self, address, param=None):
        self.server.send_message(address, param)
        time.sleep(self._WAIT_TIME)

    def _query(self, address):
        self.send(address)
        time.sleep(self._WAIT_TIME)
        return self.info_response

    def __exit__(self, exc_type, exc_value, exc_tr):
        self.server.shutdown()


def _make_remote(kind: kinds.MR18KindMap) -> MAirRemote:
    """
    Creates a new MAIR remote class.

    The returned class will subclass MAirRemote.
    """

    def init(self, *args, **kwargs):
        defaultkwargs = {"ip": None, "port": None}
        kwargs = defaultkwargs | kwargs
        MAirRemote.__init__(self, *args, **kwargs)
        self.kind = kind
        self.lr = LR.make(self)
        self.strip = tuple(Strip.make(self, i) for i in range(kind.num_strip))
        self.bus = tuple(Bus.make(self, i) for i in range(kind.num_bus))
        self.dca = tuple(DCA(self, i) for i in range(kind.num_dca))
        self.fxsend = tuple(FXSend.make(self, i) for i in range(kind.num_fx))
        self.fxreturn = tuple(FXReturn(self, i) for i in range(kind.num_fx))
        self.config = Config.make(self)
        self.aux = Aux.make(self)
        self.rtn = tuple(Rtn.make(self, i) for i in range(kind.num_rtn))

    return type(
        f"MAirRemote{kind.id_}",
        (MAirRemote,),
        {
            "__init__": init,
        },
    )


_remotes = {kind.id_: _make_remote(kind) for kind in kinds.all}


def connect(kind_id: str, *args, **kwargs):
    MAIRREMOTE_cls = _remotes[kind_id]
    return MAIRREMOTE_cls(*args, **kwargs)
