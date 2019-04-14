# Python companion to Low Speed Aerodynamics 
Low Speed Aerodynamics 2nd Edition by Joseph Katz and Alan Plotkin

## Purpose
This is a Python module that implements the computer programs listed in *Low Speed Aerodynamics (2nd Ed)*.

## Programs

| No. |   Name   |                    Program Description                | Section |
|:---:|:--------:|:-----------------------------------------------------:|:-------:|
|     |          |                  **_2D Panel Methods_**               |         |
|  1. |  `AFGEN` | Grid generator for van de Vooren airfoil shapes       |   6.7   |
|     |          |            **_2D: Neumann Boundary Condition_**       |         |
|  2. |  `VOR2D` | Discrete vortex, thin wing method                     |  11.1.1 |
|  3. | `SORC2D` | Constant strength source method                       |  11.2.1 |
|  4. | `DUB2DC` | Constant strength doublet method                      |  11.2.2 |
|  5. | `VOR2DC` | Constant strength vortex method                       |  11.2.3 |
|  6. | `SOR2DL` | Linear strength source method                         |  11.4.1 |
|  7. | `VOR2DL` | Linear strength vortex method                         |  11.4.2 |
|     |          |          **_2D: Dirichlet Boundary Condition_**       |         |
|  8. |  `PHICD` | Constant strength doublet method                      |  11.3.2 |
|  9. | `PHICSD` | Constant strength source/doublet method               |  11.3.1 |
| 10. |  `PHILD` | Linear strength doublet method                        |  11.5.2 |
| 11. |  `PHIQD` | Quadratic strength doublet method                     |  11.6.2 |
|     |          |                    **_3D Programs_**                  |         |
| 12. | `DUB3DC` | Influence of constant strength source/doublet         |  10.4.1 |
| 13. | `VORING` | VLM for rectilinear surfaces (with ground effect)     |  12.3   |
| 14. | ` PANEL` | Constant strength sources and doublets (Dirichlet BC) |  12.5   |
|     |          |             **_Time Dependent Programs_**             |         |
| 15. |   `WAKE` | Acceleration of flat plate using a lumped vortex      |  13.7   |
| 16. |   `UVLM` | Unsteady motion of a thin rectangular lifting surface |  13.12  |