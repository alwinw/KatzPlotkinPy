#!/usr/bin/python3

import collections

from katzplotkinpy.src.cli import parse_args

__VersionInfo = collections.namedtuple("VersionInfo", ("major", "minor", "micro"))

__version__ = "0.0.2"
__version_info__ = __VersionInfo(*(map(int, __version__.split("."))))

del collections, __VersionInfo
