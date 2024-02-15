import sys
import threading
from dataclasses import dataclass

import xair_api
from xair_api import kinds

kind_id = "MR18"
ip = "mixer.local"

tests = xair_api.connect(kind_id, ip=ip)

kind = kinds.get(kind_id)


@dataclass
class Data:
    """bounds test data to a kind"""

    name: str = kind.id_
    dca: int = kind.num_dca - 1
    strip: int = kind.num_strip - 1
    bus: int = kind.num_bus - 1
    fx: int = kind.num_fx - 1


data = Data()


def setup_module():
    print(f"\nRunning tests for kind [{data.name}]\n", file=sys.stdout)
    tests.worker = threading.Thread(target=tests.run_server)
    tests.worker.daemon = True
    tests.worker.start()
    tests.validate_connection()


def teardown_module():
    tests.server.shutdown()
