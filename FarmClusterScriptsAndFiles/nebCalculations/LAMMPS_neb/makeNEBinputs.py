#!/usr/bin/env python
# coding: utf-8
import sys
import os

nAtoms = 432
startfileformat = "lammpsdump"
finalfileformat = "lammpsdump"
start_filename = str(sys.argv[1])
final_filename = str(sys.argv[2])
directory = os.getcwd()

startfile = directory + "/" + start_filename
startfile_out = startfile[:-4] + ".out"
finalfile = directory + "/" + final_filename
finalfile_out = finalfile[:-4] + ".out"
startatoms = {}
endatoms = {}

#Need to make startfile into a file format appropriate for LAMMP's read_data command
if startfileformat == "lammpsdump":
	lines = open(startfile).read().splitlines()
	for n, line in enumerate(lines):
		newline = line.split()
		if n == 3:
			nAtoms = int(newline[0])
		if n == 5:
			xMin = float(newline[0])
			xMax = float(newline[1])
		if n == 6:
			yMin = float(newline[0])
			yMax = float(newline[1])
		if n == 7:
			zMin = float(newline[0])
			zMax = float(newline[1])
		elif n>=9:
			startatoms[int(newline[0])] = [float(newline[2]), float(newline[3]), float(newline[4])]

	#Output in the new file format
	o = open(startfile_out, 'w+')
	o.write('DFT Data File\n\n' + str(nAtoms) + ' atoms\n\n1 atom types\n\n')
	xsize = xMax - xMin
	ysize = yMax - yMin
	zsize = zMax - zMin
	o.write('0.0 ' + str(xsize) + ' xlo xhi\n')
	o.write('0.0 ' + str(ysize) + ' ylo yhi\n')
	o.write('0.0 ' + str(zsize) + ' zlo zhi\n')
	o.write('\nMasses\n\n1 28.085\n\nAtoms\n\n')
	for i in startatoms.items():
		atomType = 1
		blankline = [str(i[0])]
		blankline.extend(i[1])
		separator = '\t'
		final_line = separator.join(blankline)
		o.write(final_line + "\n")
	o.close()

if finalfileformat == "lammpsdump":
	lines = open(finalfile).read().splitlines()
	for n, line in enumerate(lines):
		newline = line.split()
		if n>=9:
			finalatoms[int(newline[0])] = [float(newline[2]), float(newline[3]), float(newline[4])]
			if startatoms[int(newline[0])] != finalatoms[int(newline[0)]:
				print(newline[0] + "\n")

	#Output in the new file format
	o = open(finalfile_out, 'w+')
	o.write(str(nAtoms) + "\n")
	for i in finalatoms.items():
		blankline = [str(j) for j in i[1]]
		separator = '\t'
		final_line = separator.join(blankline)
		o.write(final_line + "\n")
	o.close()
