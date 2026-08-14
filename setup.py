#!/usr/bin/env python
import sys
from pathlib import Path

from setuptools import setup

sys.path.insert(0, str(Path(__file__).resolve().parent))
import versioneer

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
