#!/usr/bin/env python3
# ---------------------------------------------------------
# Test for utility functions
# Copyright 2019 Alwin Wang
# =========================================================

import unittest

from katzplotkinpy.src.utils import get_args, vprint, get_version


class TestUtils(unittest.TestCase):
    def test_get_args(self):
        args_test = [
            ("program", "AFGEN"),
            ("input_file", "input"),
            ("quiet", "-q", True),
            ("silent", "-s", True),
            ("verbose", "-vv", 2),
            ("debug", "-d", 3),
            ("version", "-V", True),
        ]
        args_parse = get_args(args=[a[1] for a in args_test], program=True)
        self.assertEqual({a[0]: a[-1] for a in args_test}, vars(args_parse))

