C     PROGRAM No. 15: SUDDEN ACCELERATION OF A FLAT PLATE (LUMPED VORTEX)
C     ----------------------------------------------------------------
C     TRANSIENT AERODYNAMIC OF A FLAT PLATE REPRESENTED BY A SINGLE LUMPED
C     VORTEX ELEMENT (PREPARED AS A SOLUTION OF HOMEWORK PROBLEMS BY JOE
C     KATZ, 1987).
      DIMENSION VORTIC(50,3),UW(50,2)
C                   VORTIC(IT,X,Z,GAMMA)
      COMMON/NO1/ IT,VORTIC

      NSTEP=20
      PAY=3.141592654
      RO=1.
      UT=50.0
      C=1.0
      ALFA1=5.0
      ALFA=ALFA1*PAY/180.0
      SN=SIN(ALFA)
      CS=COS(ALFA)
      DT=C/UT/4.0
      T=-DT
      DXW=0.3*UT*DT
      WRITE(6,11)

C     PROGRAM START

      DO 100 IT=1,NSTEP
         T=T+DT
C        PATH OF ORIGIN (SX,SZ)
         SX=-UT*T
         SZ=0.0
C        SHEDDING OF WAKE POINTS
         VORTIC(IT,1)=(C+DXW)*CS+SX
         VORTIC(IT,2)=-(C+DXW)*SN+SZ

C        CALCULATE MOMENTARY VORTEX STRENGTH OF WING AND WAKE VORTICES

         A=-1/(PAY*C)
         B=1/(2.0*PAY*(C/4.0+DXW))
         RHS2=0.0
         WWAKE=0.0
         IF(IT.EQ.1) GOTO 2
         IT1=IT-1

C        CALCULATE WAKE INFLUENCE
         XX1=0.75*C*CS+SX
         ZZ1=-0.75*C*SN+SZ
         CALL DWASH(XX1,ZZ1,1,IT1,U,W)
         WWAKE=U*SN+W*CS

C        CALCULATION OF RHS
         DO 1 I=1,IT1
    1    RHS2=RHS2-VORTIC(I,3)
    2    CONTINUE
         RHS1=-UT*SN-WWAKE

C        SOLUTION (BASED ON ALGEBRAIC SOLUTION OF TWO EQUATIONS FOR GAMMAT
C        AND THE LATEST WAKE VORTEX STRENGTH VORTIC(IT,3).
         VORTIC(IT,3)=1/(B/A-1.0)*(RHS1/A-RHS2)
         GAMMAT=RHS2-VORTIC(IT,3)

C        WAKE ROLLUP

         IF(IT.LT.1) GOTO 5
         DO 3 I=1,IT
            XX1=0.25*C*CS+SX
            ZZ1=-0.25*C*SN+SZ
            CALL VOR2D(VORTIC(I,1),VORTIC(I,2),XX1,ZZ1,GAMMAT,U,W)
            CALL DWASH(VORTIC(I,1),VORTIC(I,2),1,IT,U1,W1)
            U=U+U1
            W=W+W1
            UW(I,1)=VORTIC(I,1)+U*DT
            UW(I,2)=VORTIC(I,2)+W*DT
    3    CONTINUE
         DO 4 I=1,IT
            VORTIC(I,1)=UW(I,1)
    4    VORTIC(I,2)=UW(I,2)
    5    CONTINUE

C        AERODYNAMIC LOADS

         IF(IT.EQ.1) GAMAT1=0.0
         QUE=0.5*RO*UT*UT
         DGAMDT=(GAMMAT-GAMAT1)/DT
         GAMAT1=GAMMAT
C        CALCULATE WAKE INDUCED DOWNWASH
         XX1=0.75*C*CS+SX
         ZZ1=-0.75*C*SN+SZ
         CALL DWASH(XX1,ZZ1,1,IT,U,W)
         WW=U*SN+W*CS
         L=RO*(UT*GAMMAT+DGAMDT*C)
         D=RO*(-WW*GAMMAT+DGAMDT*C*SN)
         CL=L/QUE/C
         CD=D/QUE/C

C        OUTPUT

         CLT=CL/(2.0*PAY*SN)
         GAM1=GAMMAT/(PAY*UT*C*SN)
         SX1=SX-UT*DT
         WRITE(6,10) IT,SX1,CD,CL,GAM1,CLT

  100 CONTINUE
   10 FORMAT(I3,10F7.3)
   11 FORMAT(' SUDDEN ACCELARATION OF A FLAT PLATE',/,38('='),//,
     *' IT',4X,'SX',5X,'CD',5X,'CL',3X,'GAMMAT',3X,'CLT')
      STOP
      END

      SUBROUTINE DWASH(X,Z,I1,I2,U,W)
C     CALCULATES DOWNWASH INDUCED BY IT-1 WAKE VORTICES
         DIMENSION VORTIC(50,3)
         COMMON/NO1/ IT,VORTIC
         U=0.0
         W=0.0
         DO 1 I=I1,I2
            CALL VOR2D(X,Z,VORTIC(I,1),VORTIC(I,2),VORTIC(I,3),U1,W1)
            U=U+U1
            W=W+W1
    1    CONTINUE
         RETURN
      END

      SUBROUTINE VOR2D(X,Z,X1,Z1,GAMMA,U,W)
C     CALCULATES INFLUENCE OF VORTEX AT (X1,Z1)
         PAY=3.141592654
         U=0.0
         W=0.0
         RX=X-X1
         RZ=Z-Z1
         R=SQRT(RX**2+RZ**2)
         IF(R.LT.0.001) GOTO 1
         V=0.5/PAY*GAMMA/R
         U=V*(RZ/R)
         W=V*(-RX/R)
    1    CONTINUE
         RETURN
      END
