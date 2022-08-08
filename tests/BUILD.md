# Appendix D Fortran  Programs

## Build

Requires CMake >= 3.5

```console
cd tests/
cmake . -B build && cmake --build build
```

## Running

```console
#> rm AFOIL2.DAT CP.DAT
#> build/AFGEN
 READY TO START VAN DE VOOREN TRANSFORMATION
 ENTER THICKNESS COEFF. E
0.15
 ENTER T.E. ANGLE COEFF. K
2
 ENTER THE ANGLE OF ATTACK IN DEGREES
0
 ENTER NUMBER OF AIRFOIL PANELS,M
 WITH WHICH TO MODEL THE AIRFOIL
 (NOTE THAT M SHOULD BE AN EVEN FACTOR OF 360)
30
Note: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG IEEE_UNDERFLOW_FLAG
#> python3 ../f77/afgenvis.py AFOIL2.DAT
```
