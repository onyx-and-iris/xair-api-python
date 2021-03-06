import mair
from mair import kinds
import threading
from dataclasses import dataclass
import sys

kind_id = "MR18"
ip = "mixer.local"

tests = mair.connect(kind_id, ip=ip)

kind = kinds.get(kind_id)


@dataclass
class Data:
    """bounds data to map tests to a kind"""

    name: str = kind.id_
    dca: int = kind.num_dca - 1
    strip: int = kind.num_strip - 1
    bus: int = kind.num_bus - 1
    fx: int = kind.num_fx - 1
    rtn: int = kind.num_rtn - 1


data = Data()


def setup_module():
    print(f"\nRunning tests for kind [{data.name}]\n", file=sys.stdout)
    tests.worker = threading.Thread(target=tests.run_server)
    tests.worker.daemon = True
    tests.worker.start()
    tests.validate_connection()


def teardown_module():
    tests.server.shutdown()
