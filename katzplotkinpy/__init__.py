#!/usr/bin/env python3
# ---------------------------------------------------------
# Main script entry for katzplotkinpy
# Copyright 2019 Alwin Wang
# =========================================================

import collections

__VersionInfo = collections.namedtuple("VersionInfo", ("major", "minor", "micro"))

__version__ = "0.0.1"
__version_info__ = __VersionInfo(*(map(int, __version__.split("."))))

del collections, __VersionInfo
