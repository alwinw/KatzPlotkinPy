#!/usr/bin/env python3
# ---------------------------------------------------------
# Grid generator for van de Vooren airfoil shapes
# Copyright 2019 Alwin Wang
# =========================================================

try:
    import katzplotkinpy.src.utils as utils
except ModuleNotFoundError:
    print("Using relative module import")
    import utils

if __name__ == "__main__":
    description = "Grid generator for van de Vooren airfoil shapes"
    args = utils.get_args(description)

    utils.vprint(1, "1 verbosity")
    utils.vprint(2, "2 verbosity")
    utils.vprint(3, "3 verbosity")
    utils.vprint(4, "4 verbosity")
    utils.vprint(5, "5 verbosity")
