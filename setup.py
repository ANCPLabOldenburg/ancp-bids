#!/usr/bin/env python
import sys, os
from setuptools import setup
import versioneer

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 30.3.0']
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []
INSTALL_REQUIRES = []

if __name__ == '__main__':
    REQ_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/requirements.txt"
    with open(REQ_FILE_PATH) as f:
        INSTALL_REQUIRES = list(f.read().splitlines())
    setup(name="ancpbids",
          version=versioneer.get_version(),
          cmdclass=versioneer.get_cmdclass(),
          setup_requires=SETUP_REQUIRES,
          install_requires=INSTALL_REQUIRES)
