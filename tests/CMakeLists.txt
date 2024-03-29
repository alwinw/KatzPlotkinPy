cmake_minimum_required(VERSION 3.5)

project(katzplotkinpy)
enable_language(Fortran)

if(CMAKE_Fortran_COMPILER_ID MATCHES "GNU")
  set(dialect "-ffixed-form -ffixed-line-length-132 -std=legacy")
  set(bounds "-fcheck=bounds")
endif()

if(CMAKE_Fortran_COMPILER_ID MATCHES "Intel")
  set(dialect "-fixed -extend-source 132 -stand none")
  set(bounds "-check bounds")
endif()

if(CMAKE_Fortran_COMPILER_ID MATCHES "PGI")
  set(dialect "--Mfixed -Mextend")
  set(bounds "-C")
endif()

set(CMAKE_Fortran_FLAGS_DEBUG "${CMAKE_Fortran_FLAGS_DEBUG} ${bounds}")
set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} ${dialect}")

#
# Compile.
#
# file(GLOB_RECURSE sources f77/*.f77)
# add_executable(prog ${sources})
add_executable(AFGEN f77/AFGEN.f)

# 2D Panel Methods
add_executable(VOR2D f77/VOR2D.f f77/LINALG.f)
add_executable(SOR2DC f77/SOR2DC.f f77/LINALG.f)
add_executable(DUB2DC f77/DUB2DC.f f77/LINALG.f)
add_executable(VOR2DC f77/VOR2DC.f f77/LINALG.f)
add_executable(SOR2DL f77/SOR2DL.f f77/LINALG.f)
add_executable(VOR2DL f77/VOR2DL.f f77/LINALG.f)

# 2D: Dirichlet Boundary Condition
add_executable(PHICD f77/PHICD.f f77/LINALG.f)
add_executable(PHICSD f77/PHICSD.f f77/LINALG.f)
add_executable(PHILD f77/PHILD.f f77/LINALG.f)
add_executable(PHIQD f77/PHIQD.f f77/LINALG.f)

# 3D Programs
add_executable(DUB3DC f77/DUB3DC.f)
add_executable(VORING f77/VORING.f f77/LINALG.f)
add_executable(PANEL f77/PANEL.f f77/LINALG.f)

# Time Dependent Programs
add_executable(WAKE f77/WAKE.f)
add_executable(UVLM f77/UVLM.f f77/LINALG.f)
