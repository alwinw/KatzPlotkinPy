from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


def vor2d(
    x: float, z: float, x1: float, z1: float, gamma: float
) -> Tuple[float, float]:
    """
    Calculates the influence of a vortex at (x1, z1).

    Parameters
    ----------
    x : float
        X-coordinate of the point where the influence is calculated.
    z : float
        Z-coordinate of the point where the influence is calculated.
    x1 : float
        X-coordinate of the vortex point.
    z1 : float
        Z-coordinate of the vortex point.
    gamma : float
        Circulation strength of the vortex.

    Returns
    -------
    Tuple[float, float]
        The influence (u, w) at the point (x, z).
    """
    pay = np.pi
    rx = x - x1
    rz = z - z1
    r = np.sqrt(rx**2 + rz**2)

    if r < 0.001:
        return 0.0, 0.0

    v = 0.5 / pay * gamma / r
    u = v * (rz / r)
    w = v * (-rx / r)

    return u, w


def decomp(n: int, a: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    LU decomposition of matrix A.

    Parameters
    ----------
    n : int
        The order of the matrix.
    a : np.ndarray
        The matrix to decompose.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        The LU-decomposed matrix and the pivot indices.
    """
    from scipy.linalg import lu_factor

    return lu_factor(a)


def solver(
    n: int, lu_and_piv: Tuple[np.ndarray, np.ndarray], b: np.ndarray
) -> np.ndarray:
    """
    Solves the linear system Ax = b using LU decomposition.

    Parameters
    ----------
    n : int
        The order of the matrix.
    lu_and_piv : Tuple[np.ndarray, np.ndarray]
        The LU-decomposed matrix and the pivot indices.
    b : np.ndarray
        The right-hand side vector.

    Returns
    -------
    np.ndarray
        The solution vector.
    """
    from scipy.linalg import lu_solve

    return lu_solve(lu_and_piv, b)


def discrete_vortex_method(
    n: int, c: float, epsilon: float, alfa1: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    """
    Discrete Vortex Method for thin airfoils with elliptic camber.

    Parameters
    ----------
    n : int
        Number of panels.
    c : float
        Chord length.
    epsilon : float
        Camber parameter.
    alfa1 : float
        Angle of attack in degrees.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray, float, float]
        X-coordinates, DCP, DCP1, CL, CL1
    """
    pay = np.pi
    alfa = alfa1 * pay / 180.0
    ro = 1.0
    v = 1.0
    uinf = np.cos(alfa) * v
    winf = np.sin(alfa) * v
    que = 0.5 * ro * v * v

    # Grid generation (N panels)
    dx = c / n
    xc = np.array([c / n * (i - 0.25) for i in range(1, n + 1)])
    zc = 4.0 * epsilon * xc / c * (1.0 - xc / c)
    x = np.array([c / n * (i - 0.75) for i in range(1, n + 1)])
    z = 4.0 * epsilon * x / c * (1.0 - x / c)
    detadx = 4.0 * epsilon / c * (1.0 - 2.0 * xc / c)
    sq = np.sqrt(1 + detadx**2)
    enx = -detadx / sq
    enz = 1.0 / sq

    # Influence coefficients
    a = np.zeros((n, n))
    gamma = np.zeros(n)
    for i in range(n):
        for j in range(n):
            u, w = vor2d(xc[i], zc[i], x[j], z[j], 1.0)
            a[i, j] = u * enx[i] + w * enz[i]
        gamma[i] = -uinf * enx[i] - winf * enz[i]

    # Solution of the problem: RHS(i) = A(i, j) * GAMMA(i)
    lu_and_piv = decomp(n, a)
    gamma = solver(n, lu_and_piv, gamma)

    # Aerodynamic loads
    dl = ro * v * gamma
    dcp = dl / dx / que
    dd = 32.0 * epsilon / c * np.sqrt(x / c * (1.0 - x / c))
    dcp1 = 4.0 * np.sqrt((c - x) / x) * alfa + dd
    bl = np.sum(dl)
    cl = bl / (que * c)
    cl1 = 2.0 * pay * (alfa + 2 * epsilon / c)

    return x, dcp, dcp1, cl, cl1


def plot_results(
    x: np.ndarray,
    dcp: np.ndarray,
    dcp1: np.ndarray,
    cl: float,
    cl1: float,
    alfa1: float,
    n: int,
) -> None:
    """
    Plots the results of the Discrete Vortex Method.

    Parameters
    ----------
    x : np.ndarray
        X-coordinates.
    dcp : np.ndarray
        Discrete pressure coefficient.
    dcp1 : np.ndarray
        Exact pressure coefficient.
    cl : float
        Lift coefficient.
    cl1 : float
        Exact lift coefficient.
    alfa1 : float
        Angle of attack in degrees.
    n : int
        Number of panels.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x, dcp, "bo-", label="DCP (Discrete)")
    plt.plot(x, dcp1, "r--", label="DCP (Exact)")
    plt.xlabel("X")
    plt.ylabel("DCP")
    plt.title(
        f"Thin Airfoil with Elliptic Camber\nCL = {cl:.3f}, CL (Exact) = {cl1:.3f}, N = {n}, Alpha = {alfa1:.1f}"
    )
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Parameters
    n = 10
    c = 1.0
    epsilon = 0.1 * c
    alfa1 = 10.0

    # Run the Discrete Vortex Method
    x, dcp, dcp1, cl, cl1 = discrete_vortex_method(n, c, epsilon, alfa1)

    # Output results
    print("Thin Airfoil with Elliptic Camber")
    print(
        f"V = 1.0, CL = {cl:.3f}, CL (Exact) = {cl1:.3f}, N = {n}, Alpha = {alfa1:.1f}"
    )
    for i in range(n):
        print(
            f"{i+1:5d}  X = {x[i]:8.2f}  DCP = {dcp[i]:8.2f}  DCP (Exact) = {dcp1[i]:6.2f}"
        )

    # Plot results
    plot_results(x, dcp, dcp1, cl, cl1, alfa1, n)
