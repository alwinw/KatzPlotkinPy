#!/usr/bin/env python3

import argparse
import logging
from collections import namedtuple

import numpy

logger = logging.getLogger(__name__)


def interactive_inputs(
    e: float = None, k: float = None, alpha: float = None, m: int = None
):
    InputVar = namedtuple("InputVars", ["name", "value", "description", "type"])

    input_vars = [
        InputVar("e", e, "Thickness Coef", float),
        InputVar("ak", k, "T.E. Angle Coef", float),
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


def afgen(e: float, k: float, alpha: float, m: int):
    """Generates van de Vooren Airfoil. Refer to Section 6.7

    :param e: Thickness coefficient
    :type e: float
    :param ak: Trailing edge angle coefficient
    :type ak: float
    :param alpha: Angle of attack (deg)
    :type alpha: float
    :param m: Number of panels
    :type m: int
    """
    logger.info(
        "Starting van de Vooren Transformation with "
        + f"e = '{e}', ak = '{k}', alpha = '{alpha}', m = '{m}'"
    )
    tl = 1.0  # l
    a = 2 * tl * (e + 1) ** (k - 1) / (2 ** k)  # Eq (6.73) ref Eq. (6.63)
    al = alpha / 57.2957795131
    try:
        m = int(m)
    except ValueError:
        logger.critical(f"Expected int or int-like, not m = '{m}'")
        raise

    theta = range(0, 1)


if __name__ == "__main__":
    afgen(1, 1, 1, 1)
