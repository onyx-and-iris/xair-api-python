import subprocess
from pathlib import Path


def test_xair():
    path = Path.cwd() / "tests" / "xair"
    subprocess.run(["pytest", "-v", str(path)])


def test_x32():
    path = Path.cwd() / "tests" / "x32"
    subprocess.run(["pytest", "-v", str(path)])
