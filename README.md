# Python companion to Low Speed Aerodynamics

[![License: GPL v3](https://img.shields.io/github/tag-pre/AlwinW/KatzPlotkinPy.svg?style=popout-square&label=Release&color=informational)](https://www.gnu.org/licenses/gpl-3.0)

[Low Speed Aerodynamics 2nd Edition](https://www.amazon.com/Low-Speed-Aerodynamics-Second-Cambridge-Aerospace/dp/0521665523) by Joseph Katz and Alan Plotkin

## Purpose

This is a project implements the FORTRAN computer programs listed in *Low Speed Aerodynamics (2nd Ed)* into a Python package and stand alone program(s). Additional features such as visualisation have been included.

Written permission provided by Professor Joseph Katz, San Diego State University, to recreate the original FORTRAN functionality in Python and/or C for this Open Source Software.

## Installation and Usage

### Installation

### Usage

A program can be used as a group of programs or individually.

```text
katzplotkinpy [OPTIONS] PROGRAM INPUT

Required:
    PROGRAM                 Name of program, e.g. VOR2D
    INPUT                   Input file

Options:
    -h, --help            show this help message and exit
    -q, --quiet           suppress messages to stdout
    -s, --silent          suppress messages to stdout
    -v, --verbose         increase output verbosity to stout (max verbosity is -vvv)
    -d, --debug           output additional messages to stout (equivalent to -vvv)
    -V, --version         Show the version and exit
```

## Programs and Features

### Programs

The following table is a summary from Appendix D of *Low Speed Aerodynamics*. Each program has been recreated in Python.

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

### Features

In addition to recreating the programs in Python, visualisation and other features have been added.

## Copyright and License

(c) 2019 Alwin Wang. All content is under Creative Commons Attribution [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.txt) and all code is under [BSD-3 clause](LICENSE)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=popout-square)](https://www.gnu.org/licenses/gpl-3.0)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=popout-square)](https://creativecommons.org/licenses/by/4.0/)