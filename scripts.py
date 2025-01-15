import subprocess
import sys
from pathlib import Path


def ex_obs():
    subprocess.run(["tox", "r", "-e", "obs"])


def ex_sends():
    path = Path.cwd() / "examples" / "sends" / "."
    subprocess.run([sys.executable, str(path)])


def ex_headamp():
    path = Path.cwd() / "examples" / "headamp" / "."
    subprocess.run([sys.executable, str(path)])


def test_xair():
    path = Path.cwd() / "tests" / "xair"
    subprocess.run(["pytest", "-v", str(path)])


def test_x32():
    path = Path.cwd() / "tests" / "x32"
    subprocess.run(["pytest", "-v", str(path)])


def test_all():
    subprocess.run(["tox"])
