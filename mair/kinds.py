from dataclasses import dataclass


@dataclass
class MR18KindMap:
    id_: str = "MR18"
    num_dca: int = 4
    num_strip: int = 16
    num_bus: int = 6
    num_fx: int = 4
    num_rtn: int = 4


_kinds = {
    "XR18": MR18KindMap(),
    "MR18": MR18KindMap(),
}

all = list(kind for kind in _kinds.values())
