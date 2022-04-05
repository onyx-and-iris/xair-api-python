import mair
from mair import kinds
import threading

_kind = 'MR18'

mars = {kind.id_: mair.connect(_kind) for kind in kinds.all}
tests = mars[_kind]

def setup_package():
    tests.worker = threading.Thread(target = tests.run_server)
    tests.worker.daemon = True
    tests.worker.start()
    tests.validate_connection()

def teardown_package():
    tests.server.shutdown()
