#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)

from katzplotkinpy.src.utils import parse_args

if __name__ == "__main__":
    args = parse_args(
        description="Python companion to Low Speed Aerodynamics", get_logger=logger
    )
