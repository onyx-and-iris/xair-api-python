import abc
import logging
import threading
import time
from pathlib import Path
from typing import Optional, Union

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_server import BlockingOSCUDPServer

from . import adapter, kinds
from .bus import Bus
from .config import Config
from .dca import DCA
from .errors import XAirRemoteError
from .fx import FX, FXSend
from .kinds import KindMap
from .lr import LR
from .rtn import AuxRtn, FxRtn
from .strip import Strip


class OSCClientServer(BlockingOSCUDPServer):
    def __init__(self, address: str, dispatcher: Dispatcher):
        super().__init__(("", 0), dispatcher)
        self.xr_address = address

    def send_message(self, address: str, vals: Optional[Union[str, list]]):
        builder = OscMessageBuilder(address=address)
        vals = vals if vals is not None else []
        if not isinstance(vals, list):
            vals = [vals]
        for val in vals:
            builder.add_arg(val)
        msg = builder.build()
        self.socket.sendto(msg.dgram, self.xr_address)


class XAirRemote(abc.ABC):
    """Handles the communication with the mixer via the OSC protocol"""

    logger = logging.getLogger("xair.xairremote")

    _CONNECT_TIMEOUT = 0.5

    _info_response = []

    def __init__(self, **kwargs):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.msg_handler)
        self.xair_ip = kwargs["ip"] or self._ip_from_toml()
        self.xair_port = kwargs["port"]
        self._delay = kwargs["delay"]
        if not self.xair_ip:
            raise XAirRemoteError("No valid ip detected")
        self.server = OSCClientServer((self.xair_ip, self.xair_port), dispatcher)

    def __enter__(self):
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
        if not self.info_response:
            raise XAirRemoteError(
                "Failed to setup OSC connection to mixer. Please check for correct ip address."
            )
        print(
            f"Successfully connected to {self.info_response[2]} at {self.info_response[0]}."
        )

    @property
    def info_response(self):
        return self._info_response

    def run_server(self):
        self.server.serve_forever()

    def msg_handler(self, addr, *data):
        self.logger.debug(f"received: {addr} {data if data else ''}")
        self._info_response = data[:]

    def send(self, addr: str, param: Optional[str] = None):
        self.logger.debug(f"sending: {addr} {param if param is not None else ''}")
        self.server.send_message(addr, param)

    def query(self, address):
        self.send(address)
        time.sleep(self._delay)
        return self.info_response

    def __exit__(self, exc_type, exc_value, exc_tr):
        self.server.shutdown()


def _make_remote(kind: KindMap) -> XAirRemote:
    """
    Creates a new XAIR remote class.

    The returned class will subclass XAirRemote.
    """

    def init_x32(self, *args, **kwargs):
        defaultkwargs = {"ip": None, "port": 10023, "delay": 0.02}
        kwargs = defaultkwargs | kwargs
        XAirRemote.__init__(self, *args, **kwargs)
        self.kind = kind
        self.mainst = adapter.MainStereo.make(self)
        self.mainmono = adapter.MainMono.make(self)
        self.matrix = tuple(
            adapter.Matrix.make(self, i) for i in range(kind.num_matrix)
        )
        self.strip = tuple(Strip.make(self, i) for i in range(kind.num_strip))
        self.bus = tuple(adapter.Bus.make(self, i) for i in range(kind.num_bus))
        self.dca = tuple(DCA(self, i) for i in range(kind.num_dca))
        self.fx = tuple(FX(self, i) for i in range(kind.num_fx))
        self.fxreturn = tuple(adapter.FxRtn.make(self, i) for i in range(kind.num_fx))
        self.auxin = tuple(adapter.AuxRtn.make(self, i) for i in range(kind.num_auxrtn))
        self.config = Config.make(self)

    def init_xair(self, *args, **kwargs):
        defaultkwargs = {"ip": None, "port": 10024, "delay": 0.02}
        kwargs = defaultkwargs | kwargs
        XAirRemote.__init__(self, *args, **kwargs)
        self.kind = kind
        self.lr = LR.make(self)
        self.strip = tuple(Strip.make(self, i) for i in range(kind.num_strip))
        self.bus = tuple(Bus.make(self, i) for i in range(kind.num_bus))
        self.dca = tuple(DCA(self, i) for i in range(kind.num_dca))
        self.fx = tuple(FX(self, i) for i in range(kind.num_fx))
        self.fxsend = tuple(FXSend.make(self, i) for i in range(kind.num_fx))
        self.fxreturn = tuple(FxRtn.make(self, i) for i in range(kind.num_fx))
        self.auxreturn = AuxRtn.make(self)
        self.config = Config.make(self)

    if kind.id_ == "X32":
        return type(
            f"XAirRemote{kind}",
            (XAirRemote,),
            {
                "__init__": init_x32,
            },
        )
    return type(
        f"XAirRemote{kind}",
        (XAirRemote,),
        {
            "__init__": init_xair,
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
