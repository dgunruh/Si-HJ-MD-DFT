#!/usr/bin/env python
# coding: utf-8
import sys
import os

nAtoms = 216

directory = os.getcwd()
input_file_extension = '/gap2.out'
inputfile = directory + input_file_extension

output_file_extension = '/gap2LAMMPS.out'
outputfile = directory + output_file_extension

num_lines = sum(1 for line in open(inputfile))

o = open(outputfile, 'w+')
o.write('DFT Data File\n\n' + str(nAtoms) + ' atoms\n\n1 atom types\n\n')

lines = open(inputfile).read().splitlines()
for n, line in enumerate(lines):
	if n == 37:
		newline = line.split()
		print(newline)
		basisLength = float(newline[4])*.529177 #convert from bohrs to angstroms
	if n == 52:
		newline = line.split()
		xSize = float(newline[1])*.529177
		ySize = float(newline[1])*.529177
		zSize = float(newline[5])*basisLength

		o.write('0.0 ' + str(xSize) + ' xlo xhi\n')
		o.write('0.0 ' + str(ySize) + ' ylo yhi\n')
		o.write('0.0 ' + str(zSize) + ' zlo zhi\n')
		o.write('\nMasses\n\n1 28.085\n\nAtoms\n\n')
	if n >= num_lines - 55 - nAtoms and n < num_lines - 55:
		newline = line.split()
		atomID = n%(num_lines - 56 - nAtoms)
		atomType = 1
		blankLine = [str(atomID)]
		blankLine.append(str(atomType))
		blankLine.append(newline[1])
		blankLine.append(newline[2])
		blankLine.append(newline[3])
		separator = '\t'
		final_line = separator.join(blankLine)
		o.write(final_line + "\n")

