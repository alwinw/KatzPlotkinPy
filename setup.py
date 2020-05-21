#!/usr/bin/env python3

import re

from setuptools import find_packages, setup

from katzplotkinpy import __version__

setup(
    name="katzplotkinpy",
    version=__version__,
    author="Alwin Wang",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlwinW/KatzPlotkinPy",
    packages=["katzplotkinpy", "katzplotkinpy.src"],
)
