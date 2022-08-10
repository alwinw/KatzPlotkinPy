import numpy as np


def vor2d(n: int, c: float, alpha: float, rho: float, v: float):
    """Discrete Vortex Method

    :param n: number of panels
    :type n: int
    :param c: chord length
    :type c: float
    :param alpha: angle of attack (deg)
    :type alpha: float
    :param rho: density (kg/m^3)
    :type rho: float
    :param v: velocity (m/s)
    :type v: float
    """
    epsilon = 0.1 * c
    alpha = np.deg2rad(alpha)

    u_inf = np.cos(alpha) * v
    w_inf = np.sin(alpha) * v
    q = 0.5 * rho * np.power(v, 2)

    xc = np.arange(0, c, c / n) + c / (4 * n)
    zc = 4 * epsilon
