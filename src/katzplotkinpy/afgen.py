import logging

import numpy as np

logger = logging.getLogger(__name__)

# TODO: Implement Joukowski Transformation


def van_de_vooren(epsilon: float, k: float, alpha: float, m: int):
    """Generates van de Vooren Airfoil. Refer to Section 6.7

    :param epsilon: Thickness coefficient (between 0 and 1)
    :type epsilon: float
    :param k: Trailing edge angle coefficient
    :type k: float
    :param alpha: Angle of attack (deg)
    :type alpha: float
    :param m: Number of panels
    :type m: int
    """
    # logger.info(
    #     f"Starting van de Vooren Transformation with {e=}, {k=}, {alpha=}, {m=}"
    # )

    # Parameters
    len = 1.0  # Half chord of the airfoil
    a = 2 * len * np.power(epsilon + 1, k - 1) / np.power(2, k)  # Eq. 6.65
    theta = np.linspace(0, 2 * np.pi, m)
    # tau = np.pi * (2 - k)

    # circle $f = a e^{-i \theta}$
    # A direct transformation on the imaginary plane is performed using Eq. 6.62
    # Alternatively equations 6.74a and 6.74b could be used on the real plane
    circle = a * np.cos(theta) + a * 1j * np.sin(theta)
    airfoil = (
        np.power(circle - a, k) / np.power(circle - a * epsilon, k - 1) + len
    )  # Eq 6.62

    # TODO: airfoil coordinate transformation with alpha

    return airfoil.real, airfoil.imag


if __name__ == "__main__":
    van_de_vooren(0.15, 2, 0, 30)
