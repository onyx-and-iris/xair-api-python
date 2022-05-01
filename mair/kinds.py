from dataclasses import dataclass

"""
# osc slightly different, interface would need adjusting to support this mixer.

@dataclass
class X32KindMap:
    id_: str = "X32"
    num_dca: int = 8
    num_strip: int = 32
    num_bus: int = 16
    num_fx: int = 8
    num_rtn: int = 6
"""


@dataclass
class MR18KindMap:
    # note ch 17-18 defined as aux rtn
    id_: str
    num_dca: int = 4
    num_strip: int = 16
    num_bus: int = 6
    num_fx: int = 4
    num_rtn: int = 4


@dataclass
class XR16KindMap:
    id_: str
    num_dca: int = 4
    num_strip: int = 16
    num_bus: int = 4
    num_fx: int = 4
    num_rtn: int = 4


@dataclass
class XR12KindMap:
    id_: str
    num_dca: int = 4
    num_strip: int = 12
    num_bus: int = 2
    num_fx: int = 4
    num_rtn: int = 4


_kinds = {
    "XR18": MR18KindMap(id_="XR18"),
    "MR18": MR18KindMap(id_="MR18"),
    "XR16": XR16KindMap(id_="XR16"),
    "XR12": XR12KindMap(id_="XR12"),
}


def get(kind_id):
    return _kinds[kind_id]


all = list(kind for kind in _kinds.values())
