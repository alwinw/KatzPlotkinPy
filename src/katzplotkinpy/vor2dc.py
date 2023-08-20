# C PROGRAM No. 5: CONSTANT STRENGTH VORTEX C
# ---------------------------------------
# C THIS PROGRAM FINDS THE PRESSURE DISTRIBUTION ON AN ARBITRARY AIRFOIL
# C BY REPRESENTING THE SURFACE AS A FINITE NUMBER OF VORTEX PANELS WITH
# C CONST. STRENGTH (NEUMANN B.C., PROGRAM BY STEVEN YON, 1989)[^1^][1].

import numpy as np

# REAL EP(400,2),EPT(400,2),PT1(400,2),PT2(400,2)
# REAL CO(400,2),A(400,400),B(400,400),G(400)
# REAL VEL(400),VELT(400),TH(400),DL(400)

EP = np.zeros((401, 2))
EPT = np.zeros((401, 2))
PT1 = np.zeros((401, 2))
PT2 = np.zeros((401, 2))
CO = np.zeros((401, 2))
A = np.zeros((401, 401))
B = np.zeros((401, 401))
G = np.zeros(401)
VEL = np.zeros(401)
VELT = np.zeros(401)
TH = np.zeros(401)
DL = np.zeros(401)

# OPEN(8,FILE='CPV.DAT',STATUS='NEW')
# OPEN(9,FILE='AFOIL2.DAT',STATUS='OLD')

f8 = open('CPV.DAT', 'w')
f9 = open('AFOIL2.DAT', 'r')

# WRITE(6,*) 'ENTER NUMBER OF PANELS'
# READ(5,*) M

M = int(input('ENTER NUMBER OF PANELS\n'))

N=M+1

# WRITE(6,*) 'ENTER ANGLE OF ATTACK IN DEGREES'
# READ(5,*) ALPHA

ALPHA = float(input('ENTER ANGLE OF ATTACK IN DEGREES\n'))

AL=ALPHA/57.2958

# C READ IN THE PANEL END POINTS
# DO I=1,M+1
# READ(9,*) EPT(I,1),EPT(I,2)
# END DO

for I in range(N):
    EPT[I] = [float(x) for x in f9.readline().split()]

# C CONVERT PANELING TO CLOCKWISE
# DO I=1,N
# EP(I,1)=EPT(N-I+1,1)
# EP(I,2)=EPT(N-I+1,2)
# END DO

EP = EPT[::-1]

# C ESTABLISH COORDINATES OF PANEL END POINTS
# DO I=1,M
# PT1(I,1)=EP(I,1)
# PT2(I,1)=EP(I+1,1)
# PT1(I,2)=EP(I,2)
# PT2(I,2)=EP(I+1,2)
# END DO

PT1[:,0] = EP[:-1,0]
PT2[:,0] = EP[1:,0]
PT1[:,1] = EP[:-1,1]
PT2[:,1] = EP[1:,1]

# C FIND PANEL ANGLES TH(J)
# DO I=1,M
# DZ=PT2(I,2)-PT1(I,2)
# DX=PT2(I,1)-PT1(I,1)
# TH(I)=ATAN2(DZ,DX)
# END DO

DZ = PT2[:, 1] - PT1[:, 1]
DX = PT2[:, 0] - PT1[:, 0]
TH = np.arctan2(DZ, DX)

# C ESTABLISH COLLOCATION POINTS
# DO I=1,M
# CO(I,1)=(PT2(I,1)-PT1(I,1))/2+PT1(I,1)
# CO(I,2)=(PT2(I,2)-PT1(I,2))/2+PT1(I,2)
# END DO

CO[:,0] = (PT2[:,0] - PT1[:,0])/2 + PT1[:,0]
CO[:,1] = (PT2[:, 0] - PT1[:, 0]) / 2 + PT1[:, 0]

# C ESTABLISH INFLUENCE COEFFICIENTS
# DO I=1,M
# DO J=I,M+!


# C CONVERT COLLOCATION POINT INTO LOCAL PANEL COORDS.
# X2T=PT2(J,1)-PT! (J,! )
# Z!T=PT! (J,! )-P! ! (J,! )
# XT=CO(I,1)-PT! (J,! )
# ZT=CO(I,2)-PT! (J,! )
# X2=X!T*COS(TH(J))+Z!T*SIN(TH(J))
# Z2=0
# X=XT*COS(TH(J))+ZT*SIN(TH(J))
# Z=-XT*SIN(TH(J))+ZT*COS(TH(J))

X2T = PT2[J, 0] - PT1[J, 0]
Z2T = PT2[J, 1] - PT1[J, 1]
XT = CO[I, 0] - PT1[J, 0]
ZT = CO[I, 1] - PT1[J, 1]
X2 = X2T * np.cos(TH[J]) + Z2T * np.sin(TH[J])
Z2 = 0
X = XT * np.cos(TH[J]) + ZT * np.sin(TH[J])
Z = -XT * np.sin(TH[J]) + ZT * np.cos(TH[J])

# C SAVE PANEL LENGTHS FOR LATER USE
# IF(I.EQ.1) THEN
# DL(J)=X!
# END IF

if I == 0:
    DL[J] = X2

# R! =SQRT(X**! +Z**! )
# R! =SQRT((X-X!)**! +Z**! )
# TH! =ATAN! (Z,X)
# TH! =ATAN! (Z,X-X!)
# IF(I.EQ.J) THEN
# UL=0.5
# WL=0
# ELSE
# UL=0.!9!6*(TH!-TH!)
# WL=0.!9!6*LOG(R!/R!)
# END IF

R1 = np.sqrt(X**2 + Z**2)
R2 = np.sqrt((X - X2)**2 + Z**2)
TH1 = np.arctan2(Z, X)
TH2 = np.arctan2(Z, X - X2)
if I == J:
    UL = 0.5
    WL = 0
else:
    UL = 0.15916 * (TH2 - TH1)
    WL = 0.15916 * np.log(R2 / R1)

# U=UL*COS(-TH(J))+WL*SIN(-TH(J))
# W=-UL*SIN(-TH(J))+WL*COS(-TH(J))

U = UL * np.cos(-TH[J]) + WL * np.sin(-TH[J])
W = -UL * np.sin(-TH[J]) + WL * np.cos(-TH[J])

# C A(I,J) IS THE COMPONENT OF VELOCITY NORMAL TO
# C THE AIRFOIL INDUCED BY THE JTH PANEL AT THE
# C ITH COLLOCATION POINT.

A[I,J]=-U*np.sin(TH[I])+W*np.cos(TH[I])

# A(I,N)=COS(AL)*SIN(TH(I))-SIN(AL)*COS(TH(I))

A[:,N-1] = np.cos(AL) * np.sin(TH) - np.sin(AL) * np.cos(TH)

# C REPLACE EQUATION M/4 WITH A KUTTA CONDITION
# DO J=I,M+!

for J in range(M//4, N):

# A(M/4,J)=0

    A[M//4,J] = 0

# END DO

# A(M/4,! )=!
# A(M/4,M)=!

A[M//4,0] = 1
A[M//4,M-1] = 1

# C SOLVE FOR THE SOLUTION VECTOR OF VORTEX STRENGTHS
# CALL MATRX(A,N,G)

G = np.linalg.solve(A[:N,:N], A[:N,N-1])

# C CONVERT SOURCE STRENGTHS INTO TANGENTIAL
# C VELOCITIES ALONG THE AIRFOIL SURFACE AND CP'S
# C ON EACH OF THE PANELS

CL=0

# !00 CONTINUE

for I in range(M):

# TEMP=0
# DO J=! ,M
# TEMP=TEMP+B(I,J)*G(J)
# END DO

    TEMP = B[I,:M].dot(G[:M])

    # VEL(I)=TEMP+COS(AL)*COS(TH(I))+SIN(AL)*SIN(TH(I))
    # CL=CL+VEL(I)*DL(I)

    VEL[I] = TEMP + np.cos(AL) * np.cos(TH[I
