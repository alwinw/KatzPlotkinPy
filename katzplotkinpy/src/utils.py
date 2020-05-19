#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def existing_file(input_path: str, allowed_extensions: tuple = None) -> Path:
    """Check if the input path points to an existing file of given (optional) extension

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
    """Check if input path points to an existing directory

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


class BootstrapArgparse:
    """Wrap argparse with commonly used CLI
    """

    def __init__(self, description: str = __package__, version: str = "0.1.0"):
        formatter_class = argparse.RawTextHelpFormatter
        self.parser = argparse.ArgumentParser(
            description=description,
            formatter_class=formatter_class,
            epilog="Source: https://github.com/AlwinW/KatzPlotkinPy",
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            required=False,
            help="Increase log verbosity (max -vvv)",
            dest="verbose_count",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            required=False,
            help="Show debugging messages (eqv. to -vv, overrides verbosity flag)",
        )
        self.parser.add_argument(
            "-s",
            "--silent",
            action="store_true",
            required=False,
            help="Suppress log warning and lower messages (overrides other verbosity flags)",
        )
        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version="%(prog)s {}".format(version),
            help="show the version and exit",
        )

    def add_input_file_arg(
        self,
        *name_or_flags: str,
        extensions: Tuple[str] = None,
        help: str = "Input file path",
    ):
        self.parser.add_argument(
            *name_or_flags,
            action="store",
            type=lambda path: existing_file(path, extensions),
            help=help,
        )

    def add_input_dir_arg(
        self, *name_or_flags: str, help: str = "Input directory path"
    ):
        self.parser.add_argument(
            *name_or_flags, action="store", type=existing_dir, help=help
        )

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def parse_args(self, get_logger: logging.Logger = None) -> argparse.Namespace:
        """
        "Parse provided args

        :param get_logger: logger to set level, defaults to None
        :type get_logger: logging.Logger, optional
        :return: args as Namespace
        :rtype: argparse.Namespace
        """
        args = self.parser.parse_args()
        if get_logger is not None:
            if args.silent:
                logger.setLevel(logging.ERROR)
            elif args.debug:
                logger.setLevel(logging.DEBUG)
            else:
                logger.setLevel(max(3 - args.verbose_count, 1) * 10)
        return args


if __name__ == "__main__":
    logging.basicConfig(format="%(name)s [%(levelname)s] %(message)s")

    cli = BootstrapArgparse()
    args = cli.parse_args(logger)

    print("Args from CLI were '{}'".format(args))

    logger.debug("Logger DEBUG")
    logger.info("Logger INFO")
    logger.warning("Logger WARNING")
    logger.error("Logger ERROR")
    logger.critical("Logger CRITICAL")
