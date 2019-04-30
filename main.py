#!/usr/bin/env python3
# ---------------------------------------------------------
# Main script entry for katzplotkinpy
# Copyright 2019 Alwin Wang
# =========================================================

import re
from katzplotkinpy.src import utils


def main():
    """
    Main function of katzplotkinpy

    If -V argument, just return the version number and exit
    """
    description = "Programs from *Low Speed Aerodynamics* Appendix D"
    args = utils.get_args(description, main=True)
    utils.verbosity(args)

    version_str = utils.get_version()
    if args.version:
        print(version_str)
        return
    utils.vprint(1, version_str)

    return args


if __name__ == "__main__":
    args = main()

    utils.vprint(3, args)
