#!/usr/bin/env python3
# ---------------------------------------------------------
# Setup file
# Copyright 2019 Alwin Wang
# =========================================================

import re
from setuptools import setup, find_packages
from katzplotkinpy.utils import get_version

setup(
    name="katzplotkinpy",
    version=get_version(),
    author="Alwin Wang",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlwinW/KatzPlotkinPy",
    packages=["katzplotkinpy", "katzplotkinpy.src"],
)

