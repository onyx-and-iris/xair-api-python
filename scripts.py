import subprocess
import sys
from pathlib import Path


def ex_obs():
    path = Path.cwd() / "examples" / "xair_obs" / "."
    subprocess.run([sys.executable, str(path)])


def test_xair():
    path = Path.cwd() / "tests" / "xair"
    subprocess.run(["pytest", "-v", str(path)])


def test_x32():
    path = Path.cwd() / "tests" / "x32"
    subprocess.run(["pytest", "-v", str(path)])
