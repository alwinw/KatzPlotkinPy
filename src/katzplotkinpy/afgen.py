# Python program No. 1: Grid generator for 2-D airfoils
# -----------------------------------------------------
# This program is an automated complex airfoil transformation of the
# type presented by Van de Vooren and De Jong (1970). The resulting
# airfoil may have a non-zero trailing edge angle. This formulation
# is for non-cambered airfoils only (programmed by Steven Yon, 1989)[^1^][1].

import numpy as np

# Open files for writing the airfoil coordinates and pressure distribution
afoil2 = open("AFOIL2.DAT", "w")
cp = open("CP.DAT", "w")

print("Ready to start Van de Vooren transformation")
print("Enter thickness coeff. E")
e = float(input())  # Read the thickness coefficient
print("Enter T.E. angle coeff. K")
ak = float(input())  # Read the trailing edge angle coefficient
tl = 1.0  # Set the chord length to 1.0
a = 2 * tl * (e + 1) ** (ak - 1) / (2**ak)  # Calculate a constant
print("Enter the angle of attack in degrees")
alpha = float(input())  # Read the angle of attack
al = alpha * np.pi / 180  # Convert to radians
print("Enter number of airfoil panels,M")
print("with which to model the airfoil")
print("(Note that M should be an even factor of 360)")
m = int(input())  # Read the number of panels
itheta = 360 // m  # Calculate the angular interval

# The loop will run through the circle plane with
# the specified angular interval and transform each
# point to the airfoil plane
for i in range(0, 361, itheta):
    if i == 0 or i == 360:  # Special case for leading and trailing edge points
        x = 1  # Set x-coordinate to 1
        y = 0  # Set y-coordinate to 0
        cp_value = 1  # Set pressure coefficient to 1
        afoil2.write(f"{x} , {y}\n")  # Write coordinates to file
        if (
            ak == 2 and i == 0
        ):  # Skip writing pressure coefficient for leading edge point if ak = 2
            continue
        if (
            ak == 2 and i == 360
        ):  # Skip writing pressure coefficient for trailing edge point if ak = 2
            continue
        cp.write(f"{x} , {cp_value}\n")  # Write pressure coefficient to file
    else:  # General case for other points on the circle plane
        th = i * np.pi / 180  # Convert angle to radians
        r1 = np.sqrt(
            (a * (np.cos(th) - 1)) ** 2 + (a * np.sin(th)) ** 2
        )  # Calculate radius from origin to point on circle plane
        r2 = np.sqrt(
            (a * (np.cos(th) - e)) ** 2 + (a * np.sin(th)) ** 2
        )  # Calculate radius from origin to point on transformed circle plane
        if th == 0:
            th1 = (
                np.pi / 2
            )  # Set angle from origin to point on circle plane to pi/2 if th = 0
        else:
            th1 = (
                np.arctan((a * np.sin(th)) / (a * (np.cos(th) - 1))) + np.pi
            )  # Calculate angle from origin to point on circle plane

        # Calculate angle from origin to point on transformed circle plane based on
        # quadrant conditions
        if np.cos(th) - e < 0 and np.sin(th) > 0:
            th2 = np.arctan((a * np.sin(th)) / (a * (np.cos(th) - e))) + np.pi
        elif np.cos(th) - e < 0 and np.sin(th) < 0:
            th2 = np.arctan((a * np.sin(th)) / (a * (np.cos(th) - e))) + np.pi
        elif np.cos(th) - e > 0 and np.sin(th) < 0:
            th2 = np.arctan((a * np.sin(th)) / (a * (np.cos(th) - e))) + 2 * np.pi
        else:
            th2 = np.arctan((a * np.sin(th)) / (a * (np.cos(th) - e)))

        # This part computes the transformed positions
        com1 = ((r1**ak) / (r2 ** (ak - 1))) / (
            (np.cos((ak - 1) * th2)) ** 2 + (np.sin((ak - 1) * th2)) ** 2
        )
        x = (
            com1
            * (
                np.cos(ak * th1) * np.cos((ak - 1) * th2)
                + np.sin(ak * th1) * np.sin((ak - 1) * th2)
            )
            + tl
        )
        y = com1 * (
            np.sin(ak * th1) * np.cos((ak - 1) * th2)
            - np.cos(ak * th1) * np.sin((ak - 1) * th2)
        )
        afoil2.write(f"{x} , {y}\n")  # Write coordinates to file

        # This part computes the transformed pressure distribution
        a1 = np.cos((ak - 1) * th1) * np.cos(ak * th2) + np.sin(
            (ak - 1) * th1
        ) * np.sin(ak * th2)
        b1 = np.sin((ak - 1) * th1) * np.cos(ak * th2) - np.cos(
            (ak - 1) * th1
        ) * np.sin(ak * th2)
        c1 = (np.cos(ak * th2)) ** 2 + (np.sin(ak * th2)) ** 2
        p = a * (1 - ak + ak * e)
        d1 = a1 * (a * np.cos(th) - p) - b1 * a * np.sin(th)
        d2 = a1 * a * np.sin(th) + b1 * (a * np.cos(th) - p)
        temp = 2 * c1 * (np.sin(al) - np.sin(al - th)) / (d1**2 + d2**2)
        com2 = temp * (r2**ak) / (r1 ** (ak - 1))
        vx = d1 * np.sin(th) + d2 * np.cos(th)
        vy = -(d1 * np.cos(th) - d2 * np.sin(th))
        cp_value = 1 - com2**2 * (vx**2 + vy**2)
        cp.write(f"{x} , {cp_value}\n")  # Write pressure coefficient to file

# Close the files
afoil2.close()
cp.close()
