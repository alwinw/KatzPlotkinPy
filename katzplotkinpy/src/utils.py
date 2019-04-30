#!/usr/bin/env python3
# ---------------------------------------------------------
# Utility functions
# Copyright 2019 Alwin Wang
# =========================================================

import re
import argparse
import logging
from pathlib import Path
from sys import argv


## Handle Command Line Interface
class InputError(Exception):
    """Exception class for command line errors"""

    pass


def get_args(description: str = "", program: bool = False, args=None):
    """
    Command Line Interface
    
    Set description in help [-h] option and return arguments entered by the user.
    """
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description="Katz and Plotkin for Python: {}".format(description),
        epilog="Source: https://github.com/AlwinW/KatzPlotkinPy",
    )
    if program:
        parser.add_argument(
            "program",
            help="program to be run",
            choices=[
                "AFGEN",
                "VOR2D",
                "SORC2D",
                "DUB2DC",
                "VOR2DC",
                "SOR2DL",
                "VOR2DL",
                "PHICD",
                "PHICSD",
                "PHILD",
                "PHIQD",
                "DUB3DC",
                "VORING",
                "PANEL",
                "WAKE",
                "UVLM",
            ],
        )
    parser.add_argument(
        "input_file",
        help="path to input file to be processed",
        type=str,
        action="store",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="suppress messages to stdout",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--silent",
        help="suppress messages to stdout",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity to stout (max verbosity is -vvv)",
        required=False,
        action="count",
        default=0,
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="output additional messages to stout (equivalent to -vvv)",
        required=False,
        action="store_const",
        const=3,
        default=0,
    )
    parser.add_argument(
        "-V",
        "--version",
        help="Show the version and exit",
        required=False,
        action="store_true",
    )
    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


## Verbosity printing
vprint = None


def verbosity(args):
    """Define verbose print function"""
    if args.verbose or args.debug:
        v = min(max(args.verbose, args.debug), 3)
        print("Verbosity level: {}".format(v))

        def _vprint(*verbosity_args):
            if verbosity_args[0] <= v:
                print(verbosity_args[1])

    else:
        _vprint = lambda *a, **k: None

    global vprint
    vprint = _vprint


## Version information
def get_version() -> str:
    """Get version information"""
    version = re.search(
        '__version__ = "([0-9.]*)"', open("katzplotkinpy/__init__.py").read()
    ).group(1)
    return "Version: {}".format(version)


## Main Function
if __name__ == "__main__":
    args = get_args("Utilities")
    verbosity(args)
    vprint(1, "hi")
