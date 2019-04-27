#!/usr/bin/env python3

# --------------------------------------
# Utility functions
# Copyright 2019 Alwin Wang and collaborators
# ======================================


import argparse
from sys import argv
from pathlib import Path


# Handle Command Line Operations
class InputError(Exception):
    pass


def get_args(description: str = ""):
    """
    Command Line Interface
    Set description in help [-h] option and return arguments entered by the user
    """
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description="Katz and Plotkin for Python: {}".format(description),
        epilog="Source: https://github.com/AlwinW/KatzPlotkinPy",
    )
    parser.add_argument(
        "input_file",
        help="path to input file to be processed",
        type=str,
        action="store",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="output additional messages to stout (equivalent to -v)",
        required=False,
        action="store_true",
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
        help="increase output verbosity to stout (e.g. -vv is more than -v)",
        required=False,
        action="count",
    )
    parser.add_argument(
        "-V",
        "--version",
        help="Show the version and exit",
        required=False,
        action="store_true",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    get_args("Utilities")
