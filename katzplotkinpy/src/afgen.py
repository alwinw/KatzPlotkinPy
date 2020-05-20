#!/usr/bin/env python3

import argparse
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

InputVar = namedtuple("InputVars", ["name", "value", "description", "type"])


def run(e: float = None, ak: float = None, alpha: float = None, m: int = None):
    logger.info("Ready to start van de Vooren Transformation")

    input_vars = [
        InputVar("e", e, "Thickness Coef", float),
        InputVar("ak", ak, "T.E. Angle Coef", float),
        InputVar("alpha", alpha, "Angle of Attack (deg)", float),
        InputVar("m", m, "Number of Panels", int),
    ]

    for input_var in input_vars:  # type:InputVar
        value = input_var.value
        if not value:
            value = input("Enter {}: ".format(input_var.description))
        try:
            value = input_var.type(value)
        except ValueError as e:
            logger.error(
                "Error while parsing input values. Got `{}` expected type `{}`".format(
                    value, input_var.type.__name__
                )
            )
            raise e
