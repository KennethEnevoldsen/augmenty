import os

from setuptools import setup

path = os.path.join("augmenty", "about.py")

with open(path) as f:
    v = f.read()
    for line in v.split("\n"):
        if line.startswith("__version__"):
            __version__ = line.split('"')[-2]


def setup_package():
    setup(version=__version__)


if __name__ == "__main__":
    setup_package()
