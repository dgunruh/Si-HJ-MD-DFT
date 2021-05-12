#!/usr/bin/env python
# coding: utf-8
import sys
import os
import numpy as np
from pathlib import Path

nAtoms = 432
startfileformat = "lammpsdump"
finalfileformat = "lammpsdump"
start_filename = str(sys.argv[1])
final_filename = str(sys.argv[2])
file_appendix = str(sys.argv[3])
home = str(Path.home())
directory = os.getcwd()

#startfile = directory + "/" + start_filename
startfile = home + "/Dropbox/HJ Project-UCD-ASU/GAP aSicSi Interface structures/" + start_filename
startfile_out = directory + "/NEB LAMMPS input files/09-08-2020 inputs/" + "neb_input_" + file_appendix + ".out"
finalfile = directory + "/" + final_filename
finalfile_out = directory + "/NEB LAMMPS input files/09-08-2020 inputs/" + "neb_end_" + file_appendix + ".out"
startatoms = {}
finalatoms = {}
count = 0
nebatoms = []

nebatom_filename = "neb_atoms_" + file_appendix + ".out"
nebatomsfile = directory + "/NEB LAMMPS input files/09-08-2020 inputs/" + nebatom_filename

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
			xsize = xMax - xMin
			ysize = yMax - yMin
			zsize = zMax - zMin
		elif n>=9:
			startatoms[int(newline[0])] = [float(newline[2])*xsize, float(newline[3])*ysize, float(newline[4])*zsize]

	#Output in the new file format
	o = open(startfile_out, 'w+')
	o.write('DFT Data File\n\n' + str(nAtoms) + ' atoms\n\n1 atom types\n\n')
	o.write('0.0 ' + str(xsize) + ' xlo xhi\n')
	o.write('0.0 ' + str(ysize) + ' ylo yhi\n')
	o.write('0.0 ' + str(zsize) + ' zlo zhi\n')
	o.write('\nMasses\n\n1 28.085\n\nAtoms\n\n')
	for i in startatoms.items():
		atomType = 1
		blankline = [str(i[0]), str(atomType)]
		blankline.extend(['{:08.7}'.format(j) for j in i[1]])
		separator = '\t'
		final_line = separator.join(blankline)
		o.write(final_line + "\n")
	o.close()

if finalfileformat == "lammpsdump":
	lines = open(finalfile).read().splitlines()
	for n, line in enumerate(lines):
		newline = line.split()
		if n>=9:
			finalatoms[int(newline[0])] = [float(newline[2])*xsize, float(newline[3])*ysize, float(newline[4])*zsize]
			altx = [i - xsize if (j == 0 and i > xsize) else i for j, i in enumerate(startatoms[int(newline[0])])]
			altx = [i + xsize if (j == 0 and i < 0) else i for j, i in enumerate(altx)]
			alty = [i - ysize if (j == 1 and i > ysize) else i for j, i in enumerate(startatoms[int(newline[0])])]
			alty = [i + ysize if (j == 1 and i < 0) else i for j, i in enumerate(alty)]
			altz = [i - zsize if (j == 2 and i > zsize) else i for j, i in enumerate(startatoms[int(newline[0])])]
			altz = [i + zsize if (j == 2 and i < 0) else i for j, i in enumerate(altz)]
			if not np.allclose(finalatoms[int(newline[0])], startatoms[int(newline[0])]) \
				and not np.allclose(finalatoms[int(newline[0])], altx) \
				and not np.allclose(finalatoms[int(newline[0])], alty) \
				and not np.allclose(finalatoms[int(newline[0])], altz):
				count += 1
				nebatoms.append(newline[0])


	#Output in the new file format
	o = open(finalfile_out, 'w+')
	o.write(str(nAtoms) + "\n")
	for i in finalatoms.items():
		blankline = [str(i[0])]
		blankline.extend(['{:08.7}'.format(j) for j in i[1]])
		separator = '\t'
		final_line = separator.join(blankline)
		o.write(final_line + "\n")
	o.close()

o = open(nebatomsfile, 'w+')
o.write(str(count) + "\n")
for i in nebatoms:
	o.write(i + "\t" + "1.0\n")
o.close()
print("Total NEB atoms: " + str(count))
