#!/usr/bin/env python3

import re
import argparse
import logging
from pathlib import Path
import sys

module = sys.modules["__main__"].__file__
# logger = logging.getLogger(module)
logger = logging.getLogger(__name__)


def parse_command_line(
    description: str = module, prog_list: bool = False, argv: list = None
) -> argparse.Namespace:
    """Parse command line arguments. See -h for details
    
    Keyword Arguments:
        argv {list} -- Arguments from command line (default: {None})
        description {str} -- Description to be presented to the user (default: {str})
    
    Returns:
        args -- Parsed arguments
    """
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog=module,
        description="Katz and Plotkin for Python: {}".format(description),
        epilog="Source: https://github.com/AlwinW/KatzPlotkinPy",
    )

    if prog_list:
        parser.add_argument(
            "program",
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
            help="program to be run",
        )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbose_count",
        default=0,
        help="Increase log verbosity for each occurance.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        required=False,
        help="Show debugging messages. Only overrules verbosity flag.",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        required=False,
        help="Suppress log messages. Overrules all other logging flags.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format("1")
    )  # ! To fix

    # TODO Additional inputs

    args = parser.parse_args()
    if args.silent:
        level = 30
    elif args.debug:
        level = 10
    else:
        level = max(3 - args.verbose_count, 0) * 10
    logger.setLevel(level)

    return args


## Main Function
if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(name)s [%(levelname)s] %(message)s",
    )

    args = parse_command_line(description="Utilities")
    logger.debug("Logger DEBUG")
    logger.info("Logger INFO")
    logger.warning("Logger WARNING")
    logger.error("Logger ERROR")
    logger.critical("Logger CRITICAL")
