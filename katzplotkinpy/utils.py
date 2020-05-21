#!/usr/bin/env python3

import argparse
import logging
import sys
from collections import namedtuple
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


prog_listing = {
    "afgen": "Grid generator for van de Vooren airfoil shapes",
    #
    "vor2d": "Discrete vortex, thin wing method",
    "sor2dc": "Constant strength source method",
    "dub2dc": "Constant strength doublet method",
    "vor2dc": "Constant strength vortex method",
    "sor2dl": "Linear strength source method",
    "vor2dl": "Linear strength vortex method",
    #
    "phicd": "Constant strength doublet method",
    "phicsd": "Constant strength source/doublet method",
    "phild": "Linear strength doublet method",
    "phiqd": "Quadratic strength doublet method",
    #
    "dub3dc": "Influence of constant strength source/doublet",
    "voring": "VLM for rectilinear surfaces (with ground effect)",
    "panel": "Constant strength sources and doublets (Dirichlet BC)",
    #
    "wake": "Acceleration of flat plate using a lumped vortex",
    "uvlm": "Unsteady motion of a thin rectangular lifting surface",
}


def existing_file(input_path: str, allowed_extensions: tuple = None) -> Path:
    """Check if the input path points to an existing file of given (optional) extension 
    and returns a Path object with expanded user

    :param input_path: path to check
    :type input_path: str
    :param allowed_extensions: allowed file type extensions as .ext, defaults to None
    :type allowed_extensions: tuple, optional
    :raises FileNotFoundError: if file does not exist
    :raises TypeError: if file extension is not one of allowed extensions
    :return: input path as a Path with expanded user
    :rtype: Path
    """
    file_path = Path(input_path)
    if not file_path.is_file():
        raise FileNotFoundError("No such file: '{}'".format(file_path))
    if allowed_extensions is not None:
        suffixes = [ext.lower() for ext in allowed_extensions]
        if file_path.suffix.lower() not in suffixes:
            raise TypeError(
                "Wrong file format: '{}' but expected '{}'".format(
                    file_path, allowed_extensions
                )
            )
    return file_path


def existing_dir(input_path: str) -> Path:
    """Check if input path points to an existing directory and returns a Path object with
    expanded user

    :param input_path: path to check
    :type input_path: str
    :raises NotADirectoryError: if path is not a directory
    :return: input path as a Path with expanded user
    :rtype: Path
    """
    dir_path = Path(input_path).expanduser()
    if not dir_path.is_dir():
        raise NotADirectoryError()
    return dir_path


def add_subparser_wrapper(
    name: str,
    subparsers: argparse._SubParsersAction,
    parents: List[argparse.ArgumentParser],
):
    return subparsers.add_parser(
        name, parents=parents, description=prog_listing[name], help=prog_listing[name]
    )


def parse_args(
    argv: List[str] = sys.argv,
    description: str = __package__,
    version: str = "0.1.0",
    get_logger: logging.Logger = None,
):

    # Main parser
    formatter_class = argparse.RawTextHelpFormatter
    main_parser = argparse.ArgumentParser(
        description=description,
        formatter_class=formatter_class,
        epilog="Source: https://github.com/AlwinW/KatzPlotkinPy",
    )
    main_parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(version),
        help="show the version and exit",
    )
    subparsers = main_parser.add_subparsers(
        title="programs",
        description="Programs from Appendix D of 'Low Speed Aerodynamics'",
        dest="program",
    )

    # Inheritance parser
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        required=False,
        help="Increase log verbosity (max -vvv)",
        dest="verbose_count",
    )
    parent_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        required=False,
        help="Show debugging messages (eqv. to -vv, overrides verbosity flag)",
    )
    parent_parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        required=False,
        help="Suppress log warning and lower messages (overrides other verbosity flags)",
    )

    # Program parsers
    afgen_parser = add_subparser_wrapper("afgen", subparsers, [parent_parser])

    vor2d_parser = add_subparser_wrapper("vor2d", subparsers, [parent_parser])
    sor2dc_parser = add_subparser_wrapper("sor2dc", subparsers, [parent_parser])
    dub2dc_parser = add_subparser_wrapper("dub2dc", subparsers, [parent_parser])
    vor2dc_parser = add_subparser_wrapper("vor2dc", subparsers, [parent_parser])
    sor2dl_parser = add_subparser_wrapper("sor2dl", subparsers, [parent_parser])
    vor2dl_parser = add_subparser_wrapper("vor2dl", subparsers, [parent_parser])

    phicd_parser = add_subparser_wrapper("phicd", subparsers, [parent_parser])
    phicsd_parser = add_subparser_wrapper("phicsd", subparsers, [parent_parser])
    phild_parser = add_subparser_wrapper("phild", subparsers, [parent_parser])
    phiqd_parser = add_subparser_wrapper("phiqd", subparsers, [parent_parser])

    dub3dc_parser = add_subparser_wrapper("dub3dc", subparsers, [parent_parser])
    voring_parser = add_subparser_wrapper("voring", subparsers, [parent_parser])
    panel_parser = add_subparser_wrapper("panel", subparsers, [parent_parser])

    wake_parser = add_subparser_wrapper("wake", subparsers, [parent_parser])
    uvlm_parser = add_subparser_wrapper("uvlm", subparsers, [parent_parser])

    if len(argv) == 1:
        main_parser.print_help(sys.stderr)
        sys.exit(1)
    args = main_parser.parse_args(argv[1:])

    if get_logger is not None:
        if args.silent:
            logger.setLevel(logging.ERROR)
        elif args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(max(3 - args.verbose_count, 1) * 10)
    return args
