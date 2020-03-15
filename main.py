#!/usr/bin/env python3

import re

from katzplotkinpy.src.utils import parse_command_line


def main():
    args = parse_command_line(
        description="Programs from *Low Speed Aerodynamics* Appendix D", prog_list=True
    )

    return None


if __name__ == "__main__":
    args = main()
