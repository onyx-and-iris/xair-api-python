from dataclasses import dataclass


@dataclass
class KindMap:
    def __str__(self) -> str:
        return self.id_


@dataclass
class X32KindMap(KindMap):
    id_: str
    num_dca: int = 8
    num_strip: int = 32
    num_bus: int = 16
    num_fx: int = 8
    num_auxrtn: int = 8
    num_matrix: int = 6


@dataclass
class XR18KindMap(KindMap):
    # note ch 17-18 defined as aux return
    id_: str
    num_dca: int = 4
    num_strip: int = 16
    num_bus: int = 6
    num_fx: int = 4


@dataclass
class XR16KindMap(KindMap):
    id_: str
    num_dca: int = 4
    num_strip: int = 16
    num_bus: int = 4
    num_fx: int = 4


@dataclass
class XR12KindMap(KindMap):
    id_: str
    num_dca: int = 4
    num_strip: int = 12
    num_bus: int = 2
    num_fx: int = 4


_kinds = {
    "X32": X32KindMap(id_="X32"),
    "MR18": XR18KindMap(id_="MR18"),
    "XR18": XR18KindMap(id_="XR18"),
    "XR16": XR16KindMap(id_="XR16"),
    "XR12": XR12KindMap(id_="XR12"),
}


def get(kind_id):
    return _kinds[kind_id]


all = list(kind for kind in _kinds.values())
