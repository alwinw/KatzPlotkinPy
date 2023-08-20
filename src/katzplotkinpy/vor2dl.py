# Python code for linear strength vortex method (arbitrary airfoil)
# Based on Fortran code by Steven Yon, 1989

import numpy as np

# Parameters
M = 10 # number of panels
C = 1.0 # chord length
EPS = 0.1 * C # camber amplitude
ALPHA = 10.0 # angle of attack in degrees
PI = np.pi # pi constant
AL = ALPHA * PI / 180.0 # angle of attack in radians
RO = 1.0 # air density
V = 1.0 # free stream velocity
UINF = np.cos(AL) * V # x-component of free stream velocity
WINF = np.sin(AL) * V # z-component of free stream velocity
QUE = 0.5 * RO * V**2 # dynamic pressure

# Arrays
EP = np.zeros((M+2, 2)) # panel end points
EPT = np.zeros((M+2, 2)) # panel end points (temp)
PT1 = np.zeros((M+1, 2)) # panel start point
PT2 = np.zeros((M+1, 2)) # panel end point
CO = np.zeros((M+1, 2)) # collocation point
A = np.zeros((M+1, M+1)) # influence coefficient matrix
B = np.zeros((M+1, M+1)) # influence coefficient matrix (temp)
G = np.zeros(M+1) # vortex strength
TH = np.zeros(M+1) # panel angle
DL = np.zeros(M+1) # lift per unit span
CP = np.zeros(M+1) # pressure coefficient
CP1 = np.zeros(M+1) # exact pressure coefficient

# Read in the panel end points from file 'AFOIL2.DAT'
with open('AFOIL2.DAT', 'r') as f:
    for i in range(1, M+2):
        EPT[i, 0], EPT[i, 1] = map(float, f.readline().split())

# Reverse the order of the panel end points
for i in range(1, M+2):
    EP[i, 0] = EPT[M-i+2, 0]
    EP[i, 1] = EPT[M-i+2, 1]

# Establish coordinates of panel end points
for i in range(1, M+1):
    PT1[i, 0] = EP[i, 0]
    PT2[i, 0] = EP[i+1, 0]
    PT1[i, 1] = EP[i, 1]
    PT2[i, 1] = EP[i+1, 1]

# Find panel angles TH(I)
for i in range(1, M+1):
    DZ = PT2[i, 1] - PT1[i, 1]
    DX = PT2[i, 0] - PT1[i, 0]
    TH[i] = np.arctan2(DZ, DX)

# Establish collocation points
for i in range(1, M+1):
    CO[i, 0] = (PT2[i, 0] - PT1[i, 0]) / 2 + PT1[i, 0]
    CO[i, 1] = (PT2[i, 1] - PT1[i, 1]) / 2 + PT1[i, 1]

# Establish influence coefficients
for i in range(1, M+1):
    for j in range(1, M+1):
        # Convert collocation point to local panel coords.
        XT = CO[i, 0] - PT1[j ,0]
        ZT = CO[i ,1] - PT1[j ,1]
        X2T= PT2[j ,0] - PT1[j ,0]
        Z2T= PT2[j ,1] - PT1[j ,1]
        X= XT * np.cos(TH[j]) + ZT * np.sin(TH[j])
        Z= -XT * np.sin(TH[j]) + ZT * np.cos(TH[j])
        X2= X2T * np.cos(TH[j]) + Z2T * np.sin(TH[j])
        Z2= 0

        # Save panel lengths for lift coeff. calc.
        if i == j:
            DL[j]= X2

        # Find Rl,RZ.THl.THZ.
        Rl= np.sqrt(X**2 + Z**2)
        RZ= np.sqrt((X-XZ)**Z + Z**Z)
        THl= np.arctan2(Z, X)
        THZ= np.arctan2(Z, X-XZ)

        # GAMMA1 and GAMMAZ. These velocities are in
        # the Jth reference frame.
        if i == j:
            U1L= -0.5 * (X-XZ) / (XZ)
            UZL= 0.5 * (X) / (XZ)
            W1L= -0.15916
            WZL= 0.15916
        else:
            U1L= -(Z * np.log(RZ / Rl) + X * (THZ - THl) - X2 * (THZ - THl)) / (6.28319 * X2)
            UZL= (Z * np.log(RZ / Rl) + X * (THZ - THl)) / (6.28319 * X2)
            W1L= -((X2 - Z * (THZ - THl)) - X * np.log(Rl / RZ) + X2 * np.log(Rl / RZ)) / (6.28319 * X2)
            WZL= ((X2 - Z * (THZ - THl)) - X * np.log(Rl / RZ)) / (6.28319 * X2)

        # Transform the local velocities into the
        # global reference frame.
        U1= U1L * np.cos(-TH[j]) + W1L * np.sin(-TH[j])[^1^][1]
        U2= U2L * np.cos(-TH[j]) + W2L * np.sin(-TH[j])
        W1= -U1L * np.sin(-TH[j]) + W1L * np.cos(-TH[j])
        W2= -U2L * np.sin(-TH[j]) + W2L * np.cos(-TH[j])

        # Compute the coefficients of GAMMA in the
        # influence matrix.
        if j == 1:
            A[i, 1] = -U1 * np.sin(TH[i]) + W1 * np.cos(TH[i])[^1^][1]
            HOLDA = -U2 * np.sin(TH[i]) + W2 * np.cos(TH[i])
            B[i, 1] = U1 * np.cos(TH[i]) + W1 * np.sin(TH[i])
            HOLDB = U2 * np.cos(TH[i]) + W2 * np.sin(TH[i])
        elif j == M:
            A[i, M] = -U1 * np.sin(TH[i]) + W1 * np.cos(TH[i]) + HOLDA[^2^][2]
            A[i, N] = -U2 * np.sin(TH[i]) + W2 * np.cos(TH[i])[^1^][1]
            B[i, M] = U1 * np.cos(TH[i]) + W1 * np.sin(TH[i]) + HOLDB[^2^][2]
            B[i, N] = U2 * np.cos(TH[i]) + W2 * np.sin(TH[i])[^1^][1]
        else:
            A[i, j] = -U1* np.sin(TH[i]) + W1* np.cos(TH[i]) + HOLDA[^1^][1]
            HOLDA = -U2* np.sin(TH[i]) + W2* np.cos(TH(i))
            B(i, j) = U1* np.cos(TH(i)) + W1* np.sin(TH(i)) + HOLDB
            HOLDB = U2* np.cos(TH(i)) + W2* np.sin(TH(i))[^2^][2]
    A(i, N+1) = np.cos(AL)* np.sin(TH(i)) - np.sin(AL)* np.cos(TH(i))

# Add the Kutta condition
A[N, 1] = 1
A[N, N] = 1

# Solve for the solution vector of vortex strengths
G = np.linalg.solve(A, G)

# Convert vortex strengths into tangential
# velocities along the airfoil surface and CP's
# on each of the panels.
CL = 0
for i in range(1, M+1):
    VEL = 0
    for j in range(1, N+1):
        VEL = VEL + B(i, j) * G(j)
    V = VEL + np.cos(AL)* np.cos(TH(i)) + np.sin(AL)* np.sin(TH(i))
    CL = CL + V* DL(i)
    CP(i) = 1- V**2

# Output to console
print('Arbitrary airfoil with linear strength vortex method')
print(f'V={V:7.3f}   CL={CL:7.3f}   N={N:6d}   ALPHA={ALPHA:6.3f}')
print(' I      X      CP')
for i in range(M):
    ...
