import abc
import threading
import time
from pathlib import Path
from typing import Optional, Self

import tomllib
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_server import BlockingOSCUDPServer

from . import kinds
from .bus import Bus
from .config import Config
from .dca import DCA
from .errors import XAirRemoteError
from .fx import FXReturn, FXSend
from .kinds import KindMap
from .lr import LR
from .rtn import Aux, Rtn
from .strip import Strip


class OSCClientServer(BlockingOSCUDPServer):
    def __init__(self, address: str, dispatcher: Dispatcher):
        super().__init__(("", 0), dispatcher)
        self.xr_address = address

    def send_message(self, address: str, value: str):
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


class XAirRemote(abc.ABC):
    """Handles the communication with the mixer via the OSC protocol"""

    _CONNECT_TIMEOUT = 0.5
    _WAIT_TIME = 0.025
    _REFRESH_TIMEOUT = 5

    XAIR_PORT = 10024

    info_response = []

    def __init__(self, **kwargs):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.msg_handler)
        self.xair_ip = kwargs["ip"] or self._ip_from_toml()
        self.xair_port = kwargs["port"] or self.XAIR_PORT
        if not (self.xair_ip and self.xair_port):
            raise XAirRemoteError("No valid ip or password detected")
        self.server = OSCClientServer((self.xair_ip, self.xair_port), dispatcher)

    def __enter__(self) -> Self:
        self.worker = threading.Thread(target=self.run_server, daemon=True)
        self.worker.start()
        self.validate_connection()
        return self

    def _ip_from_toml(self) -> str:
        filepath = Path.cwd() / "config.toml"
        with open(filepath, "rb") as f:
            conn = tomllib.load(f)
        return conn["connection"].get("ip")

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

    def send(self, address: str, param: Optional[str] = None):
        self.server.send_message(address, param)
        time.sleep(self._WAIT_TIME)

    def _query(self, address):
        self.send(address)
        time.sleep(self._WAIT_TIME)
        return self.info_response

    def __exit__(self, exc_type, exc_value, exc_tr):
        self.server.shutdown()


def _make_remote(kind: KindMap) -> XAirRemote:
    """
    Creates a new XAIR remote class.

    The returned class will subclass MAirRemote.
    """

    def init(self, *args, **kwargs):
        defaultkwargs = {"ip": None, "port": None}
        kwargs = defaultkwargs | kwargs
        XAirRemote.__init__(self, *args, **kwargs)
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
        f"XAirRemote{kind}",
        (XAirRemote,),
        {
            "__init__": init,
        },
    )


_remotes = {kind.id_: _make_remote(kind) for kind in kinds.all}


def request_remote_obj(kind_id: str, *args, **kwargs) -> XAirRemote:
    """
    Interface entry point. Wraps factory expression and handles errors

    Returns a reference to an XAirRemote class of a kind
    """
    XAIRREMOTE_cls = None
    try:
        XAIRREMOTE_cls = _remotes[kind_id]
    except ValueError as e:
        raise SystemExit(e)
    return XAIRREMOTE_cls(*args, **kwargs)
