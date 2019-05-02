#!/usr/bin/env python3
# ---------------------------------------------------------
# Complete test of KatzPlotkinPy
# Copyright 2019 Alwin Wang
# =========================================================

import os
import unittest

import katzplotkinpy


class TestAFGEN(unittest.TestCase):
    def test_afgen(self):

        module_dir = os.path.dirname(katzplotkinpy.__file__)
        test_data_dir = os.path.join(module_dir, "test", "test_data")
        output_dir = os.path.join(module_dir, "test", "test_output/")


if __name__ == "__main__":
    unittest.main()
