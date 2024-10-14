from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


def van_de_vooren_transformation(
    E: float, AK: float, ALPHA: float, M: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform the Van de Vooren transformation for a 2-D airfoil.

    Parameters
    ----------
    E : float
        Thickness coefficient (e.g. 0.15).
    AK : float
        Trailing edge angle coefficient (e.g. 2).
    ALPHA : float
        Angle of attack in degrees (e.g. 0).
    M : int
        Number of airfoil panels (must be factor of 360, e.g. 30).

    Returns
    -------
    np.ndarray
        Transformed airfoil coordinates.
    np.ndarray
        Transformed pressure distribution.
    """
    TL = 1.0
    A = 2 * TL * (E + 1) ** (AK - 1) / (2**AK)
    AL = ALPHA / 57.2958
    ITHETA = 360 // M

    airfoil_coords = []
    pressure_distribution = []

    for I in range(0, 361, ITHETA):
        if I == 0 or I == 360:
            X = 1
            Y = 0
            CP = 1
            airfoil_coords.append((X, Y))
            if AK == 2 and (I == 0 or I == 360):
                continue
            pressure_distribution.append((X, CP))
        else:
            TH = I / 57.2958
            R1 = np.sqrt((A * (np.cos(TH) - 1)) ** 2 + (A * np.sin(TH)) ** 2)
            R2 = np.sqrt((A * (np.cos(TH) - E)) ** 2 + (A * np.sin(TH)) ** 2)
            if TH == 0:
                TH1 = 1.5708
            else:
                TH1 = np.arctan((A * np.sin(TH)) / (A * (np.cos(TH) - 1))) + 3.1415927

            if np.cos(TH) - E < 0 and np.sin(TH) > 0:
                TH2 = np.arctan((A * np.sin(TH)) / (A * (np.cos(TH) - E))) + 3.1415927
            elif np.cos(TH) - E < 0 and np.sin(TH) < 0:
                TH2 = np.arctan((A * np.sin(TH)) / (A * (np.cos(TH) - E))) + 3.1415927
            elif np.cos(TH) - E > 0 and np.sin(TH) < 0:
                TH2 = (
                    np.arctan((A * np.sin(TH)) / (A * (np.cos(TH) - E))) + 2 * 3.1415927
                )
            else:
                TH2 = np.arctan((A * np.sin(TH)) / (A * (np.cos(TH) - E)))

            # Compute the transformed positions
            COM1 = ((R1**AK) / (R2 ** (AK - 1))) / (
                (np.cos((AK - 1) * TH2)) ** 2 + (np.sin((AK - 1) * TH2)) ** 2
            )
            X = (
                COM1
                * (
                    np.cos(AK * TH1) * np.cos((AK - 1) * TH2)
                    + np.sin(AK * TH1) * np.sin((AK - 1) * TH2)
                )
                + TL
            )
            Y = COM1 * (
                np.sin(AK * TH1) * np.cos((AK - 1) * TH2)
                - np.cos(AK * TH1) * np.sin((AK - 1) * TH2)
            )

            airfoil_coords.append((X, Y))

            # Compute the transformed pressure distribution
            A1 = np.cos((AK - 1) * TH1) * np.cos(AK * TH2) + np.sin(
                (AK - 1) * TH1
            ) * np.sin(AK * TH2)
            B1 = np.sin((AK - 1) * TH1) * np.cos(AK * TH2) - np.cos(
                (AK - 1) * TH1
            ) * np.sin(AK * TH2)
            C1 = (np.cos(AK * TH2)) ** 2 + (np.sin(AK * TH2)) ** 2
            P = A * (1 - AK + AK * E)
            D1 = A1 * (A * np.cos(TH) - P) - B1 * A * np.sin(TH)
            D2 = A1 * A * np.sin(TH) + B1 * (A * np.cos(TH) - P)

            TEMP = 2 * C1 * (np.sin(AL) - np.sin(AL - TH)) / (D1**2 + D2**2)
            COM2 = TEMP * (R2**AK) / (R1 ** (AK - 1))
            VX = D1 * np.sin(TH) + D2 * np.cos(TH)
            VY = -(D1 * np.cos(TH) - D2 * np.sin(TH))
            CP = 1 - COM2**2 * (VX**2 + VY**2)

            pressure_distribution.append((X, CP))

    return np.array(airfoil_coords), np.array(pressure_distribution)


def save_to_file(data: np.ndarray, filename: Path) -> None:
    """
    Save numpy array data to a file.

    Parameters
    ----------
    data : np.ndarray
        Data to be saved.
    filename : Path
        Path of the file to save the data.
    """
    np.savetxt(filename, data, delimiter=",", fmt="%f")


def plot_airfoil(airfoil_coords: np.ndarray) -> None:
    """
    Plot the airfoil coordinates.

    Parameters
    ----------
    airfoil_coords : np.ndarray
        Airfoil coordinates to be plotted.
    """
    plt.figure()
    plt.plot(airfoil_coords[:, 0], airfoil_coords[:, 1], marker="o")
    plt.title("Airfoil Shape")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()


def plot_pressure_distribution(pressure_distribution: np.ndarray) -> None:
    """
    Plot the pressure distribution.

    Parameters
    ----------
    pressure_distribution : np.ndarray
        Pressure distribution to be plotted.
    """
    plt.figure()
    plt.plot(pressure_distribution[:, 0], pressure_distribution[:, 1], marker="o")
    plt.title("Pressure Distribution")
    plt.xlabel("X")
    plt.ylabel("Cp")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    E = float(input("Enter thickness coefficient E (e.g. 0.15): "))
    AK = float(input("Enter T.E. angle coefficient K (e.g. 2): "))
    ALPHA = float(input("Enter the angle of attack in degrees (e.g. 2): "))
    M = int(input("Enter number of airfoil panels, M (factor of 360, e.g. 30): "))

    airfoil_coords, pressure_distribution = van_de_vooren_transformation(
        E, AK, ALPHA, M
    )

    save_to_file(airfoil_coords, Path("AFOIL2.DAT"))
    save_to_file(pressure_distribution, Path("CP.DAT"))

    plot_airfoil(airfoil_coords)
    plot_pressure_distribution(pressure_distribution)
