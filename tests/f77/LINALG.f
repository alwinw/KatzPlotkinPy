C     LINEAR ALGEBRA
      SUBROUTINE DECOMP(N,NDIM,A,IP)
      REAL A(NDIM,NDIM),T
      INTEGER IP(NDIM)
C     MATRIX TRIANGULARIZATION BY GAUSSIAN ELIMINATION.
C     N = ORDER OF MATRIX. NDIM = DECLARED DIMENSION OF ARRAY A.
C     A = MATRIX TO BE TRIANGULARIZED.
C     IP(K) , K .LT. N = INDEX OF K-TH PIVOT ROW.
      IP(N) = 1
      DO 6 K = 1, N
         IF(K.EQ.N) GOTO 5
         KP1 = K + 1
         M = K
         DO 1 I = KP1, N
            IF( ABS(A(I,K)).GT.ABS(A(M,K))) M=I
 1       CONTINUE

         IP(K) = M
         IF(M.NE.K) IP(N) = -IP(N)
         T = A(M,K)
         A(M,K) = A(K,K)
         A(K,K) = T
         IF(T.EQ.0.E0) GO TO 5

         DO 2 I = KP1, N
 2          A(I,K) = -A(I,K)/T
         DO 4 J = KP1, N
            T = A(M,J)
            A(M,J) = A(K,J)
            A(K,J) = T
            IF(T .EQ. 0.E0) GO TO 4
            DO 3 I = KP1, N
 3             A(I,J) = A(I,J) + A(I,K)*T
 4       CONTINUE
 5       IF(A(K,K) .EQ. 0.E0) IP(N) = 0
 6    CONTINUE
      RETURN
      END

      SUBROUTINE SOLVER(N,NDIM,A,B,IP)
      REAL A(NDIM,NDIM), B(NDIM), T
      INTEGER IP(NDIM)
C     SOLUTION OF LINEAR SYSTEM, A*X = B.
C     N = ORDER OF MATRIX.
C     NDIM = DECLARED DIMENSION OF THE ARRAY A.
C     B = RIGHT HAND SIDE VECTOR.
C     IP = PIVOT VECTOR OBTAINED FROM SUBROUTINE DECOMP.
C     B = SOLUTION VECTOR, X.

      IF(N.EQ.1) GOTO 9
      NM1 = N - 1
      DO 7 K = 1, NM1
         KP1 = K + 1
         M = IP(K)
         T = B(M)
         B(M) = B(K)
         B(K) = T
         DO 7 I = KP1, N
 7          B(I) = B(I) + A(I,K)*T

      DO 8 KB = 1, NM1
         KM1 = N - KB
         K = KM1 + 1
         B(K) = B(K)/A(K,K)
         T = -B(K)
         DO 8 I = 1, KM1
 8          B(I) = B(I) + A(I,K)*T
 9    B(1) = B(1)/A(1,1)
      RETURN
      END