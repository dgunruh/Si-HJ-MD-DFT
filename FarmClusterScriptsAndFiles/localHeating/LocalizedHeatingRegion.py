#!/usr/bin/env python
# coding: utf-8

import sys
import os

#We require the user to give the file name and the 
#atom number which they think the localized heating should be centered on
filename = str(sys.argv[1])
targetAtomNum = int(sys.argv[2]) - 1

#First get the LAMMPS file
directory = os.getcwd()
inputfile = directory + "/" + filename

#Read in all necessary information: box boundaries, and atom coordinates
atoms = []
lines = open(inputfile,"r").read().splitlines()
for n,line in enumerate(lines):
    newline = line.split()
    if n == 3:
        xMin = float(newline[0])
        xMax = float(newline[1])
    if n == 4:
        yMin = float(newline[0])
        yMax = float(newline[1])
    if n == 5:
        zMin = float(newline[0])
        zMax = float(newline[1])
    elif n > 6:
        atoms.append([float(newline[2]), float(newline[3]), float(newline[4])])

targetAtom = atoms[targetAtomNum]
#Get the closest distance of the atom to any boundary edges. Even though
#we have periodic boundary conditions, regions in lammps do not wrap around the box
maxRadius = min(targetAtom[2]-zMin, zMax - targetAtom[2], 
                targetAtom[0] - xMin, xMax - targetAtom[0],
                targetAtom[1] - yMin, yMax - targetAtom[1])

#We want the bounding sphere to be no less than 1.5 angstroms in radius
if maxRadius < 1.5:
    print("Problem, atom too close to boundary edges")
else:
    print(f"Atom coordinates: [{targetAtom[0]}, {targetAtom[1]}, {targetAtom[2]}]") 
    print(f"Sphere radius: {min(2.5, maxRadius)}")

