#!/usr/bin/env python
# coding: utf-8

import sys
import os

#specify any control parameters here
prefix = "'silicon'"
calculation = ""
nstep = 20
pseudo_dir = ""
outdir = ""
optscheme = "\"broyden\""
numImages = 7
pseudo_potential = "Si.pbe-n-kjpaw_psl.1.0.0.UPF"
ecutwfc = "44.0"
kpoints = 2

#First get the 2 LAMMPS files
directory = os.getcwd()
first_file_extension = str(sys.argv[1])
firstinputfile = directory + "/" + first_file_extension
second_file_extension = str(sys.argv[2])
secondinputfile = directory + "/" + second_file_extension

#Next create the output file
outputfile = directory + "/si." + "nebDFT" + ".in"

#Create the &PATH namelist
out = open(outputfile,'w')
out.write("BEGIN" + "\n")
out.write("BEGIN_PATH_INPUT" + "\n")
out.write("&PATH" + "\n")
out.write("  restart_mode\t= 'from_scratch'\n")
out.write("  string_method\t= 'neb',\n")
out.write("  nstep_path\t= " + str(nstep) + ",\n")
out.write("  ds\t\t= 1.D0,\n")
out.write("  opt_scheme\t= " + optscheme + ",\n")
out.write("  num_of_images\t= " + str(numImages) + ",\n")
out.write("  CI_scheme\t= \"no-CI\",\n")
out.write("  path_thr\t= 0.05D0,\n")
out.write("/\n")
out.write("END_PATH_INPUT\n")
out.write("BEGIN_ENGINE_INPUT\n")

#Now create the &CONTROL namelist

out.write("&CONTROL\n")
if prefix:
    out.write("  prefix=" + prefix + ",\n")
if calculation:
    out.write("  calculation = "+calculation+ ",\n")
if pseudo_dir:
    out.write("  pseudo_dir = "+pseudo_dir+ ",\n")
if outdir:
    out.write("  outdir = " + outdir+ ",\n")
out.write("/\n")
out.write("\n")

#Now start to read in the LAMMPS file, and create the &SYSTEM namelist
lines = open(firstinputfile,"r").read().splitlines()
for n,line in enumerate(lines):
    newline = line.split(' ')
    if n == 3:
        natoms = newline[0]
        out.write("&SYSTEM\n")
        out.write("  ibrav = 0,\n")
        out.write("  nat = " + natoms + ",\n")
        out.write("  ntyp = 1,\n")
        out.write("  ecutwfc = " + ecutwfc + ",\n")
        out.write("/\n")
        out.write("\n")

        #Now create the &ELECTRONS namelist
        out.write("&ELECTRONS\n")
        out.write("/\n")
        out.write("\n")

        #Now create the ATOMIC_SPECIES card
        out.write("ATOMIC_SPECIES\n")
        out.write("Si  28.086  " + pseudo_potential + "\n")
        out.write("\n")
    elif n ==5:
        #Now create the CELL_PARAMETERS card
        out.write("CELL_PARAMETERS { angstrom }\n")
        xSize = float(newline[1]) - float(newline[0])
    elif n == 6:
        ySize = float(newline[1]) - float(newline[0])
    elif n == 7:
        zSize = float(newline[1]) - float(newline[0])
        out.write("   " + str(xSize) + "  0  0\n")
        out.write("   0  " + str(ySize) + "  0\n")
        out.write("   0  0  " + str(zSize) + "\n")
        out.write("\n")
	
	#Now, create the K_POINTS card
        out.write("K_POINTS automatic\n")
        out.write("   " + str(kpoints) + " " + str(kpoints) + " " + str(kpoints) + "  1 1 1\n")
    elif n >= 9:
        if n == 9:
            #Now for the meat: create the atomic positions card
            out.write("BEGIN_POSITIONS\n")
            out.write("FIRST_IMAGE\n")
            out.write("ATOMIC_POSITIONS { angstrom }\n")
	    
        if len(newline) == 2:
            newarray = newline[1].split('\t')
            newline.pop()
            newline.extend(newarray)
        x = float(newline[2])*xSize
        y = float(newline[3])*ySize
        z = float(newline[4])*zSize
        out.write("   Si "+ str(x) + " " + str(y) + " " + str(z) + "\n")

lines = open(secondinputfile,"r").read().splitlines()
for n,line in enumerate(lines):
    newline = line.split(' ')
    if n >= 9:
        if n == 9:
            #Now for the meat: create the last image
            out.write("LAST_IMAGE\n")
            out.write("ATOMIC_POSITIONS { angstrom }\n")
        x = float(newline[2])*xSize
        y = float(newline[3])*ySize
        z = float(newline[4])*zSize
        out.write("   Si "+ str(x) + " " + str(y) + " " + str(z) + "\n")

out.write("END_POSITIONS\n")
out.write("END_ENGINE_INPUT\n")
out.write("END\n")
