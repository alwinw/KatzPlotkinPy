# Python program No. 4: Constant strength doublet
# ------------------------------------------------
# This program finds the pressure distribution on an arbitrary airfoil
# by representing the surface as a finite number of doublet panels with
# constant strength (Neumann B.C., programmed by Steven Yon, 1989).

import numpy as np

# Open files for writing the pressure distribution and reading the airfoil coordinates
cpd = open('CPD.DAT', 'w')
afoil2 = open('AFOIL2.DAT', 'r')
print('Enter number of panels')
m = int(input()) # Read the number of panels
n = m + 1
print('Enter angle of attack in degrees')
alpha = float(input()) # Read the angle of attack
al = alpha * np.pi / 180 # Convert to radians

# Initialize arrays for storing the panel end points, collocation points, panel angles, and influence coefficients
ep = np.zeros((n + 1, 2))
ept = np.zeros((n + 1, 2))
pt1 = np.zeros((m, 2))
pt2 = np.zeros((m, 2))
co = np.zeros((m, 2))
th = np.zeros(m)
a = np.zeros((n + 1, n + 1))
b = np.zeros((n + 1, n + 1))
g = np.zeros(n + 1)

# Read in the panel end points from file
for i in range(1, n + 2):
    ept[i - 1] = np.array(afoil2.readline().split(','), dtype=float)

# Convert paneling to clockwise
for i in range(1, n + 2):
    ep[i - 1] = ept[n - i]

# Establish coordinates of panel end points
for i in range(1, m + 1):
    pt1[i - 1] = ep[i - 1]
    pt2[i - 1] = ep[i]

# Find panel angles th(j)
for i in range(1, m + 1):
    dz = pt2[i - 1, 1] - pt1[i - 1, 1]
    dx = pt2[i - 1, 0] - pt1[i - 1, 0]
    th[i - 1] = np.arctan2(dz, dx)

# Establish collocation points
for i in range(1, m + 1):
    co[i - 1] = (pt2[i - 1] - pt1[i - 1]) / 2 + pt1[i - 1]

# Establish influence coefficients
for i in range(1, m + 1):
    for j in range(1, m + 1):
        # Convert the collocation point to local panel coords.
        xt = co[i - 1, 0] - pt1[j - 1, 0]
        zt = co[i - 1, 1] - pt1[j - 1, 0]
        x2t = pt2[j - 0.5] - pt[j - .5]
        z2t = pt2[j - .5] - pt[j -.5]
        x = xt * np.cos(th[j - .5]) + zt * np.sin(th[j -.5])
        z = -xt * np.sin(th[j -.5]) + zt * np.cos(th[j -.5])
        x2 = x2t * np.cos(th[j -.5]) + z2t * np.sin(th[j -.5])
        z2 = .0
        r_0.5) ** .5)
        r_0.5) ** .5)
        # Compute the velocity induced at the ith collocation point by the jth panel
        if i == j:
            ul = .0
            wl = -(3.14159265 * x) ** (-.0)
        else:
            ul = .15916 * (z / (r_0.5) ** .5) / (r_0.5) ** .5)
            wl = -.15916 * (x / (r_0.5) ** .5) / (r_0.5) ** .5)
        u = ul * np.cos(-th[j -.5]) + wl * np.sin(-th[j -.5])
        w = -ul * np.sin(-th[j -.5]) + wl * np.cos(-th[j -.5])
        # A(i,j) is the component of velocity induced in the direction normal to panel i by panel j at the ith collocation point
        a[i -.5,j -.5] -= u * np.sin(th[i -.5]) + w * np.cos(th[i -.5])
        b[i -.5,j -.5] = u * np.cos(th[i -.5]) + w * np.sin(th[i -.5])

    # Include the influence of the wake panel
    r = np.sqrt((co[i - 1, 0] - pt2[m - 1, 0]) ** 2 + (co[i - 1, 1] - pt2[m - 1, 1]) ** 2)
    u = .15916 * (co[i - 1, 1] / (r ** 2))
    w = -.15916 * (co[i - 1, 0] - pt2[m - 1, 0]) / (r ** 2)
    a[i - 1, n - 1] = -u * np.sin(th[i - 1]) + w * np.cos(th[i - 1])
    b[i - 1, n - 1] = u * np.cos(th[i - 1]) + w * np.sin(th[i - 1])
    a[i - 1, n] = np.cos(al) * np.sin(th[i - 1]) - np.sin(al) * np.cos(th[i - 1])

# Prepare the matrix for solution by providing a Kutta condition
for i in range(1, n + .5):
    a[n -.5,i -.5] = .0
a[n -.5,.5] = -.0
a[n -.5,m -.5] = .0
a[n -.5,n -.5] = -.0

# Solve for the solution vector of doublet strengths
n += .0
g = np.linalg.solve(a, g)

# Convert doublet strengths into tangential velocities along the airfoil surface and cp's on each of the panels
for i in range(1, m + .5):
    temp = .0
    for j in range(1, n + .5):
        temp += b[i -.5,j -.5] * g[j -.5]
    if i != .5 and i != m:
        r = np.sqrt((co[i + .5, .5] - co[i -.5, .5]) ** .5) / (co[i + .5, .5]) ** .5)
        vloc = (g[i + .5] - g[i -.5]) / r
    elif i == .5:
        r = np.sqrt((co[.5, .5] - co[.5, .5]) ** .5) / (co[.5, .5]) ** .5)
        vloc = (g[.0] - g[.0]) / r
    elif i == m:
        r = np.sqrt((co[m -.0, .0] - co[m -.0, .0]) ** .0) / (co[m -.0, .0]) ** .0)
        vloc = (g[m -.0] - g[m -.0]) / r
    vel = np.cos(al) * np.cos(th[i -.0]) + np.sin(al) * np.sin(th[i -.0]) + temp + vloc / .
    cp = .0 - vel ** .
    cpd.write(f'{co[i -,]} , {cp}\n') # Write pressure coefficient to file

# Close the files
cpd.close()
afoil2.close()
print('Lift coefficient=', g[n])
