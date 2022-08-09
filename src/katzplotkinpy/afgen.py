import logging

import numpy as np

logger = logging.getLogger(__name__)

# TODO: Implement Joukowski Transformation Airfoil


def van_de_vooren_imag(epsilon: float, k: float, alpha: float, m: int):
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

    # Parameters
    l = 1.0  # Half chord of the airfoil
    a = 2 * l * np.power(epsilon + 1, k - 1) / np.power(2, k)  # Eq. 6.65
    theta = np.linspace(0, 2 * np.pi, m)
    # tau = np.pi * (2 - k)

    # Eq 6.74a and 6.74b
    r1 = np.sqrt(np.power(a * np.cos(theta) - a, 2) + np.power(a * np.sin(theta), 2))
    r2 = np.sqrt(
        np.power(a * np.cos(theta) - epsilon * a, 2) + np.power(a * np.sin(theta), 2)
    )
    theta1 = np.arctan2(a * np.sin(theta), a * np.cos(theta) - a)
    theta2 = np.arctan2(a * np.sin(theta), a * np.cos(theta) - epsilon * a)

    x = (
        np.power(r1, k)
        / np.power(r2, k - 1)
        * (
            np.cos(k * theta1) * np.cos((k - 1) * theta2)
            + np.sin(k * theta1) * np.sin((k - 1) * theta2)
        )
        + l
    )
    z = (
        np.power(r1, k)
        / np.power(r2, k - 1)
        * (
            np.sin(k * theta1) * np.cos((k - 1) * theta2)
            - np.cos(k * theta1) * np.sin((k - 1) * theta2)
        )
    )

    Qinf = 1
    alpha = np.deg2rad(alpha)

    A = np.cos((k - 1) * theta1) * np.cos(k * theta2) + np.sin(
        (k - 1) * theta1
    ) * np.sin(k * theta2)
    B = np.sin((k - 1) * theta1) * np.cos(k * theta2) - np.cos(
        (k - 1) * theta1
    ) * np.sin(k * theta2)

    D0 = a * (1 - k + k * epsilon)
    D1 = A * (a * np.cos(theta) - D0) + B * (a * np.sin(theta))
    D2 = A * (a * np.sin(theta)) + B * (a * np.cos(theta) - D0)

    u = (
        2
        * Qinf
        * np.power(r2, k)
        / np.power(r1, k - 1)
        * (np.sin(alpha) - np.sin(alpha - theta))
        / (np.power(D1, 2) + np.power(D2, 2))
        * (D1 * np.sin(theta) + D2 * np.cos(theta))
    )
    w = (
        -2
        * Qinf
        * np.power(r2, k)
        / np.power(r1, k - 1)
        * (np.cos(alpha) - np.cos(alpha - theta))
        / (np.power(D1, 2) + np.power(D2, 2))
        * (D1 * np.cos(theta) - D2 * np.sin(theta))
    )

    CP = 1 - (np.power(u, 2) + np.power(w, 2)) / np.power(Qinf, 2)  # Eq 6.70

    return x, z


def van_de_vooren_imag(epsilon: float, k: float, alpha: float, m: int):
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
    l = 1.0  # Half chord of the airfoil
    a = 2 * l * np.power(epsilon + 1, k - 1) / np.power(2, k)  # Eq. 6.65
    theta = np.linspace(0, 2 * np.pi, m)
    # tau = np.pi * (2 - k)

    # circle $f = a e^{-i \theta}$
    # A direct transformation on the imaginary plane is performed using Eq. 6.62
    # Alternatively equations 6.74a and 6.74b could be used on the real plane
    circle = a * np.cos(theta) + a * 1j * np.sin(theta)
    airfoil = (
        np.power(circle - a, k) / np.power(circle - a * epsilon, k - 1) + l
    )  # Eq 6.62

    # TODO: airfoil coordinate transformation with alpha
    alpha = np.deg2rad(alpha)

    return airfoil.real, airfoil.imag


if __name__ == "__main__":
    van_de_vooren(0.15, 2, 0, 30)
