#!/usr/bin/env python3
# ---------------------------------------------------------
# Main script entry for katzplotkinpy
# Copyright 2019 Alwin Wang
# =========================================================

import katzplotkinpy.utils as utils

if __name__ == "__main__":
    description = "Programs from *Low Speed Aerodynamics* Appendix D"
    args = utils.get_args(description, main=True)
    utils.verbosity(args)
