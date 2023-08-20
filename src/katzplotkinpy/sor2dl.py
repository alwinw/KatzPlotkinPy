# Python program No. 6: Linear strength source
# --------------------------------------------
# This program finds the pressure distribution on an arbitrary airfoil
# by representing the surface as a finite number of source panels with
# linear strength (alpha=0, Neumann B.C., program by Steven Yon, 1989).

import numpy as np

# Define the arrays for the panel end points, collocation points, etc.
ep = np.zeros((400, 2))  # panel end points
ept = np.zeros((400, 2))  # panel end points (temp)
pt1 = np.zeros((400, 2))  # first point of each panel
pt2 = np.zeros((400, 2))  # second point of each panel
co = np.zeros((400, 2))  # collocation points
a = np.zeros((400, 400))  # influence coefficients matrix
b = np.zeros((400, 400))  # induced local tangential velocity matrix
g = np.zeros(400)  # solution vector of source strengths
v = np.zeros(400)  # tangential velocities along the airfoil surface
th = np.zeros(400)  # panel angles

# Open the files for input and output
cps = open("CPLS.DAT", "w")  # output file for cp values
afoil2 = open("AFOIL2.DAT", "r")  # input file for panel end points

# Read the number of panels from user input
m = int(input("Enter number of panels: "))
n = m + 1

# Read the option to skip the matrix reduction from user input
ans = int(input("Skip the matrix reduction? 1=YES,2=NO: "))

# Read in the panel end points from the input file
for i in range(n):
    ept[i] = np.array(afoil2.readline().split(), dtype=float)

# Convert paneling to clockwise
for i in range(n):
    ep[i] = ept[n - i - 1]

# Establish coordinates of panel end points
for i in range(m):
    pt1[i] = ep[i]
    pt2[i] = ep[i + 1]

# Find panel angles th(j)
for i in range(m):
    dz = pt2[i, 1] - pt1[i, 1]
    dx = pt2[i, 0] - pt1[i, 0]
    th[i] = np.arctan2(dz, dx)

# Establish collocation points
for i in range(m):
    co[i] = (pt2[i] - pt1[i]) / 2 + pt1[i]

# Establish influence coefficients
for i in range(m + 1):
    for j in range(m):
        # Convert collocation point to local panel coords.
        xt = co[i, 0] - pt1[j, 0]
        zt = co[i, 1] - pt1[j, 1]
        x2t = pt2[j, 0] - pt1[j, 0]
        z2t = pt2[j, 1] - pt1[j, 1]
        x = xt * np.cos(th[j]) + zt * np.sin(th[j])
        z = -xt * np.sin(th[j]) + zt * np.cos(th[j])
        x2 = x2t * np.cos(th[j]) + z2t * np.sin(th[j])
        z2 = 0

        # Find r1, r2, th1, th2
        r1 = np.sqrt(x**2 + z**2)
        r2 = np.sqrt((x - x2) ** 2 + z**2)
        th1 = np.arctan2(z, x)
        th2 = np.arctan2(z, x - x2)

        # Compute velocity components as functions of
        # sigma1 and sigma2. These velocities are in
        # the jth reference frame.
        if i == j:
            u1l = 0.15916
            u2l = -0.15916
            w1l = -0.5 * (x - x2) / x2
            w2l = 0.5 * x / x2
        else:
            w1l = -(z * np.log(r2 / r1) + x * (th2 - th1) - x2 * (th2 - th1)) / (
                6.28319 * x2
            )
            w2l = (z * np.log(r2 / r1) + x * (th2 - th1)) / (6.28319 * x2)
            u1l = (
                (x2 - z * (th2 - th1)) - x * np.log(r1 / r2) + x2 * np.log(r1 / r2)
            ) / (6.28319 * x2)
            u2l = -((x2 - z * (th2 - th1)) - x * np.log(r1 / r2)) / (6.28319 * x2)

        # Transform the local velocities into the global
        # reference frame.
        u1 = u1l * np.cos(-th[j]) + w1l * np.sin(-th[j])
        u2 = u2l * np.cos(-th[j]) + w2l * np.sin(-th[j])
        w1 = -u1l * np.sin(-th[j]) + w1l * np.cos(-th[j])
        w2 = -u2l * np.sin(-th[j]) + w2l * np.cos(-th[j])

        # A(i,j) is the influence coeff. defined by the
        # tangency condition. B(i,j) is the induced local
        # tangential velocity to be used in cp calculation.
        if j == 1:
            a[i, 1] = -u1 * np.sin(th[i]) + w1 * np.cos(th[i])
            holda = -u2 * np.sin(th[i]) + w2 * np.cos(th[i])
            b[i, 1] = u1 * np.cos(th[i]) + w1 * np.sin(th[i])
            holdb = u2 * np.cos(th[i]) + w2 * np.sin(th[i])
        elif j == m:
            a[i, m] = -u1 * np.sin(th[i]) + w1 * np.cos(th[i]) + holda
            a[i, n] = -u2 * np.sin(th[i]) + w2 * np.cos(th[i])
            b[i, m] = u1 * np.cos(th[i]) + w1 * np.sin(th[i]) + holdb
            b[i, n] = u2 * np.cos(th[i]) + w2 * np.sin(th[i])
        else:
            a[i, j] = -u1 * np.sin(th[i]) + w1 * np.cos(th[i]) + holda
            holda = -u2 * np.sin(th[i]) + w2 * np.cos(th[i])
            b[i, j] = u1 * np.cos(th[i]) + w1 * np.sin(th[i]) + holdb
            holdb = u2 * np.cos(th(i)) + w2 * np.sin(th(i))

    a[i, n - 1] = np.sin(th(i))

# Solve for the solution vector of source strengths
if ans == 1:
    # Skip the matrix reduction
    g = np.linalg.solve(a, np.zeros(m))
else:
    # Use the matrix reduction function
    g = matrx(a, n - 1)  # matrx is a user-defined function

# Convert source strengths into tangential
# velocities along the airfoil surface and cp's
# on each of the panels
for i in range(m):
    vel = 0
    for j in range(m):
        vel = vel + b[i, j] * g[j]
    v[i] = vel + np.cos(al) * np.cos(th(i)) + np.sin(al) * np.sin(th(i))
    cp = 1 - v(i) ** 2
    cps.write(f"{pt1(i,0)} , {cp}\n")

print(" ")
print("Lift coefficient=0")
