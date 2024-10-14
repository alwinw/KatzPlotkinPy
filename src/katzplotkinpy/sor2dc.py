from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


def read_panel_endpoints(file_path: Path, num_panels: int) -> np.ndarray:
    """
    Reads the panel endpoints from a file.

    Parameters
    ----------
    file_path : Path
        Path to the file containing panel endpoints.
    num_panels : int
        Number of panels.

    Returns
    -------
    np.ndarray
        Array of panel endpoints.
    """
    data = np.loadtxt(file_path, delimiter=",")
    return data[: num_panels + 1]


def convert_to_clockwise(endpoints: np.ndarray) -> np.ndarray:
    """
    Converts panel endpoints to clockwise order.

    Parameters
    ----------
    endpoints : np.ndarray
        Array of panel endpoints.

    Returns
    -------
    np.ndarray
        Array of panel endpoints in clockwise order.
    """
    return endpoints[::-1]


def establish_panel_endpoints(endpoints: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Establishes the coordinates of panel endpoints.

    Parameters
    ----------
    endpoints : np.ndarray
        Array of panel endpoints.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Arrays of panel start and end points.
    """
    pt1 = endpoints[:-1]
    pt2 = endpoints[1:]
    return pt1, pt2


def find_panel_angles(pt1: np.ndarray, pt2: np.ndarray) -> np.ndarray:
    """
    Finds the angles of the panels.

    Parameters
    ----------
    pt1 : np.ndarray
        Array of panel start points.
    pt2 : np.ndarray
        Array of panel end points.

    Returns
    -------
    np.ndarray
        Array of panel angles.
    """
    dz = pt2[:, 1] - pt1[:, 1]
    dx = pt2[:, 0] - pt1[:, 0]
    return np.arctan2(dz, dx)


def establish_collocation_points(pt1: np.ndarray, pt2: np.ndarray) -> np.ndarray:
    """
    Establishes the collocation points.

    Parameters
    ----------
    pt1 : np.ndarray
        Array of panel start points.
    pt2 : np.ndarray
        Array of panel end points.

    Returns
    -------
    np.ndarray
        Array of collocation points.
    """
    return (pt2 + pt1) / 2


def compute_influence_coefficients(
    collocation_points: np.ndarray, pt1: np.ndarray, pt2: np.ndarray, angles: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the influence coefficients.

    Parameters
    ----------
    collocation_points : np.ndarray
        Array of collocation points.
    pt1 : np.ndarray
        Array of panel start points.
    pt2 : np.ndarray
        Array of panel end points.
    angles : np.ndarray
        Array of panel angles.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Influence coefficient matrices A and B.
    """
    m = len(pt1)
    A = np.zeros((m, m + 1))
    B = np.zeros((m, m))

    for i in range(m):
        for j in range(m):
            xt = collocation_points[i, 0] - pt1[j, 0]
            zt = collocation_points[i, 1] - pt1[j, 1]
            x2t = pt2[j, 0] - pt1[j, 0]
            z2t = pt2[j, 1] - pt1[j, 1]

            x = xt * np.cos(angles[j]) + zt * np.sin(angles[j])
            z = -xt * np.sin(angles[j]) + zt * np.cos(angles[j])
            x2 = x2t * np.cos(angles[j]) + z2t * np.sin(angles[j])
            z2 = 0

            r1 = np.sqrt(x**2 + z**2)
            r2 = np.sqrt((x - x2) ** 2 + z**2)

            th1 = np.arctan2(z, x)
            th2 = np.arctan2(z, x - x2)

            if i == j:
                ul = 0
                wl = 0.5
            else:
                ul = 1 / (2 * np.pi) * np.log(r1 / r2)
                wl = 1 / (2 * np.pi) * (th2 - th1)

            u = ul * np.cos(-angles[j]) + wl * np.sin(-angles[j])
            w = -ul * np.sin(-angles[j]) + wl * np.cos(-angles[j])

            A[i, j] = -u * np.sin(angles[i]) + w * np.cos(angles[i])
            B[i, j] = u * np.cos(angles[i]) + w * np.sin(angles[i])

        A[i, m] = np.sin(angles[i])

    return A, B


def solve_source_strengths(A: np.ndarray) -> np.ndarray:
    """
    Solves for the source strengths.

    Parameters
    ----------
    A : np.ndarray
        Influence coefficient matrix A.

    Returns
    -------
    np.ndarray
        Solution vector of source strengths.
    """
    m = A.shape[0]
    b = np.zeros(m)
    return np.linalg.solve(A[:, :-1], b)


def compute_cp(
    collocation_points: np.ndarray, B: np.ndarray, G: np.ndarray, angles: np.ndarray
) -> np.ndarray:
    """
    Computes the pressure coefficients (Cp).

    Parameters
    ----------
    collocation_points : np.ndarray
        Array of collocation points.
    B : np.ndarray
        Influence coefficient matrix B.
    G : np.ndarray
        Solution vector of source strengths.
    angles : np.ndarray
        Array of panel angles.

    Returns
    -------
    np.ndarray
        Array of pressure coefficients (Cp).
    """
    m = len(collocation_points)
    cp = np.zeros(m)

    for i in range(m):
        vel = np.sum(B[i, :] * G)
        cp[i] = 1 - (vel + np.cos(angles[i])) ** 2

    return cp


def write_cp(file_path: Path, collocation_points: np.ndarray, cp: np.ndarray) -> None:
    """
    Writes the pressure coefficients to a file.

    Parameters
    ----------
    file_path : Path
        Path to the output file.
    collocation_points : np.ndarray
        Array of collocation points.
    cp : np.ndarray
        Array of pressure coefficients.
    """
    data = np.column_stack((collocation_points[:, 0], cp))
    np.savetxt(file_path, data, fmt="%.6f", delimiter=", ")


def main():
    """
    Main function to execute the program.
    """
    input_file = Path("AFOIL2.DAT")
    output_file = Path("CP.DAT")

    num_panels = int(input("ENTER NUMBER OF PANELS: "))
    skip_matrix_reduction = int(input("SKIP THE MATRIX REDUCTION? 1=YES,2=NO: "))

    endpoints = read_panel_endpoints(input_file, num_panels)
    endpoints = convert_to_clockwise(endpoints)
    pt1, pt2 = establish_panel_endpoints(endpoints)
    angles = find_panel_angles(pt1, pt2)
    collocation_points = establish_collocation_points(pt1, pt2)
    A, B = compute_influence_coefficients(collocation_points, pt1, pt2, angles)

    if skip_matrix_reduction != 1:
        G = solve_source_strengths(A)
    else:
        G = np.zeros(num_panels)

    cp = compute_cp(collocation_points, B, G, angles)
    write_cp(output_file, collocation_points, cp)

    print("LIFT COEFFICIENT=0")


if __name__ == "__main__":
    main()
