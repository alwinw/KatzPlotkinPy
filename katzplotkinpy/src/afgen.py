#!/usr/bin/env python3

import argparse
import logging
import sys

logger = logging.getLogger(__name__)

try:
    from katzplotkinpy.src.utils import parse_command_line
except ModuleNotFoundError:
    logger.warning("Using local import")
    from utils import parse_command_line


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(name)s [%(levelname)s]: %(message)s",
    )

    args = parse_command_line(
        description="Grid generator for van de Vooren airfoil shapes"
    )
