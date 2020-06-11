#!/usr/bin/env python3

import argparse
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)


def interactive_inputs(
    e: float = None, ak: float = None, alpha: float = None, m: int = None
):
    InputVar = namedtuple("InputVars", ["name", "value", "description", "type"])

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


def afgen(e: float, ak: float, alpha: float, m: int):
    logger.info("Starting van de Vooren Transformation")
    tl = 1.0
    a = 2 * tl * (e + 1.0) ** (ak - 1.0) / (2.0 ** ak)
    al = alpha / 57.2957795131
    i_theta = 360 / m
