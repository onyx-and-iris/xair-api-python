import os
import subprocess
import sys
from pathlib import Path


def ex_obs():
    subprocess.run(['tox', 'r', '-e', 'obs'])


def ex_sends():
    path = Path.cwd() / 'examples' / 'sends' / '.'
    subprocess.run([sys.executable, str(path)])


def ex_headamp():
    path = Path.cwd() / 'examples' / 'headamp' / '.'
    subprocess.run([sys.executable, str(path)])


def test_xair():
    subprocess.run(['tox'], env=os.environ.copy() | {'TEST_MODULE': 'xair'})


def test_x32():
    path = Path.cwd() / 'tools' / 'x32.exe'
    proc = subprocess.Popen([str(path), '-i', 'x32.local'])
    subprocess.run(['tox'], env=os.environ.copy() | {'TEST_MODULE': 'x32'})
    proc.terminate()


def test_all():
    steps = [test_xair, test_x32]
    for step in steps:
        step()
