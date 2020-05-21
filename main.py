#!/usr/bin/env python3

import logging

from katzplotkinpy import __version__
from katzplotkinpy.utils import parse_args

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(format="%(name)s [%(levelname)s] %(message)s")

    args = parse_args(
        description="Python companion to Low Speed Aerodynamics",
        version=__version__,
        get_logger=logger,
    )
