# Python code for discrete vortex method (thin wing, elliptic camber)
# Based on Fortran code by Joe Katz, circa 1986

import numpy as np

# Parameters
N = 10  # number of panels
C = 1.0  # chord length
EPSILON = 0.1 * C  # camber amplitude
ALFA1 = 10.0  # angle of attack in degrees
PAY = np.pi  # pi constant
ALFA = ALFA1 * PAY / 180.0  # angle of attack in radians
RO = 1.0  # air density
V = 1.0  # free stream velocity
UINF = np.cos(ALFA) * V  # x-component of free stream velocity
WINF = np.sin(ALFA) * V  # z-component of free stream velocity
QUE = 0.5 * RO * V**2  # dynamic pressure

# Arrays
GAMMA = np.zeros(N)  # vortex strength
XC = np.zeros(N)  # collocation point x-coordinate
ZC = np.zeros(N)  # collocation point z-coordinate
X = np.zeros(N)  # vortex point x-coordinate
Z = np.zeros(N)  # vortex point z-coordinate
ENX = np.zeros(N)  # normal vector x-component at collocation point
ENZ = np.zeros(N)  # normal vector z-component at collocation point
A = np.zeros((N, N))  # influence coefficient matrix
DL = np.zeros(N)  # lift per unit span
DCP = np.zeros(N)  # pressure coefficient
DCP1 = np.zeros(N)  # exact pressure coefficient

# Grid generation (N panels)
DX = C / N  # panel length
for I in range(N):
    # Collocation point
    XC[I] = C / N * (I + 0.75)
    ZC[I] = 4.0 * EPSILON * XC[I] / C * (1.0 - XC[I] / C)
    # Vortex point
    X[I] = C / N * (I + 0.25)
    Z[I] = 4.0 * EPSILON * X[I] / C * (1.0 - X[I] / C)
    # Normal vector at collocation point; N=(ENX,ENZ)
    DETADX = 4.0 * EPSILON / C * (1.0 - 2.0 * XC[I] / C)
    SQ = np.sqrt(1 + DETADX**2)
    ENX[I] = -DETADX / SQ
    ENZ[I] = 1.0 / SQ

# Influence coefficients
for I in range(N):
    for J in range(N):
        A[I, J] = vor2d(XC[I], ZC[I], X[J], Z[J], 1.0) @ np.array([ENX[I], ENZ[I]])
    # The RHS vector is placed in the GAMMA vector
    GAMMA[I] = -UINF * ENX[I] - WINF * ENZ[I]

# Solution of the problem: RHS(I)=A(I,J)*GAMMA(I)
GAMMA = np.linalg.solve(A, GAMMA)

# Aerodynamic loads
BL = 0.0
for I in range(N):
    DL[I] = RO * V * GAMMA[I]
    DCP[I] = DL[I] / DX / QUE
    # DCP1 is the analytic solution
    DD = 32.0 * EPSILON / C * np.sqrt(X[I] / C * (1.0 - X[I] / C))
    DCP1[I] = 4.0 * np.sqrt((C - X[I]) / X[I]) * ALFA + DD
    BL += DL[I]
CL = BL / (QUE * C)
CL1 = 2.0 * PAY * (ALFA + 2 * EPSILON / C)

# Output to console
print("Thin airfoil with elliptic camber")
print(
    f"V={V:7.1f}   CL={CL:7.3f}   CL(EXACT)={CL1:7.3f}   N={N:6d}   ALPHA={ALFA1:6.1f}"
)
print(" I      X      DCP     DCP(EXACT)")
for I in range(N):
    print(f"{I+1:2d} {X[I]:8.2f} {DCP[I]:8.2f} {DCP1[I]:8.2f}")

# Plotter output can be placed here (e.g., DCP and DCP1 vs X/C)


def vor2d(X, Z, X1, Z1, GAMMA):
    # Calculates influence of vortex at (X1,Z1)
    U = 0.0
    W = 0.0
    RX = X - X1
    RZ = Z - Z1
    R = np.sqrt(RX**2 + RZ**2)
    if R < 0.001:
        return np.array([U, W])
    V = 0.5 / PAY * GAMMA / R
    U = V * (RZ / R)
    W = -V * (RX / R)
    return np.array([U, W])
