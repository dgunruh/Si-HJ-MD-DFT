#!/usr/bin/env python
# coding: utf-8

import sys
import os
import numpy as np
#specify any control parameters here
prefix = "'silicon'"
dt = "30.D0"
calculation = ""
nstep = ""
pseudo_dir = "'./'"
outdir = "'./'"
pseudo_potential = "Si.pbe-hgh.UPF"
ecutwfc = "12.D0"
kpoints = 1

#structureList = [4,5,6,7,8,12,13,20,24,29,30,32,33,34,37,38,44]
for i in range(1,48):
	atom_list = []
	prefix = "'aSicSi_merged_GAP-" + str(i) + "-scf" + "'"

	#First get the LAMMPS file
	directory = os.getcwd()
	file_extension = '/../mergedInterfaces/' + 'aSicSi_merged_GAP-' + str(i) + '.xyz'
	inputfile = directory + file_extension

	if os.path.exists(inputfile):

		#Next create the output file
		outputfile = directory + "/" + "aSi_GAP_" + str(i) + ".in"

		#Now create the &CONTROL namelist
		out = open(outputfile,'w')
		out.write("&CONTROL\n")

		if calculation:
			out.write("  calculation = "+calculation+ ",\n")
		if dt:
			out.write("  dt = " + dt + ",\n")
		if prefix:
			out.write("  prefix=" + prefix + ",\n")
		if nstep:
			out.write("  nstep = "+nstep+",\n")
		if pseudo_dir:
			out.write("  pseudo_dir = "+pseudo_dir+ ",\n")
		if outdir:
			out.write("  outdir = " + outdir+ "\n")
		out.write("  wf_collect = .true.,\n")
		out.write("  verbosity = 'high',\n")
		out.write("/\n")
		out.write("\n")

		#Now start to read in the LAMMPS file, and create the &SYSTEM namelist
		lines = open(inputfile,"r").read().splitlines()
		for n,line in enumerate(lines):
			newline = line.split(' ')
			if n == 3:
				natoms = newline[0]
			elif n == 5:
				xSize = float(newline[1]) - float(newline[0])
				ySize = xSize
				out.write("&SYSTEM\n")
				out.write("  ibrav = 6,")
				out.write(" celldm(1) = " + "{:.9f}".format(xSize*1.889716164) + ",")
			elif n == 7:
				zSize = float(newline[1]) - float(newline[0])
				zRatio = zSize/xSize
				out.write(" celldm(3) = " + "{:.9f}".format(zRatio) + ",")
				out.write(" nat = " + natoms + ",")
				out.write(" ntyp = 1,\n")
				out.write("  ecutwfc\t= " + ecutwfc + ", nbnd = 1728,\n")
				out.write("  degauss\t= 0.05D0,\n")
				out.write("  occupations\t= \"smearing\",\n")
				out.write("  smearing\t= \"methfessel-paxton\",\n")
				out.write("/\n")

				#Now create the &ELECTRONS namelist
				out.write("&ELECTRONS\n")
				out.write("  electron_maxstep = 200,\n")
				out.write("  conv_thr = 1.D-6,\n")
				out.write("  mixing_beta = 0.3D0,\n")
				out.write("  scf_must_converge=.false.,\n")
				out.write("/\n")

				#Now create the &IONS namelist
				out.write("&IONS\n")
				out.write("/\n")

				#Now create the ATOMIC_SPECIES card
				out.write("ATOMIC_SPECIES\n")
				out.write("Si  28.08  " + pseudo_potential + "\n")
				out.write("K_POINTS {automatic}\n")
				out.write(str(kpoints) + " " + str(kpoints) + " " + str(kpoints) + "  0 0 0\n")
			elif n >= 9:
				if n ==9:
					#Now for the meat: create the atomic positions card
					out.write("ATOMIC_POSITIONS (angstrom)\n")
				x = float(newline[2])*xSize
				y = float(newline[3])*ySize
				z = float(newline[4])*zSize
				atom_list.append([x,y,z])
		atom_array = np.asarray(atom_list)
		sorted_atom_array = atom_array[atom_array[:,2].argsort()]
		for i in sorted_atom_array:	
			out.write("Si "+ "{:.10f}".format(i[0]) + " " + "{:.10f}".format(i[1]) + " " + "{:.10f}".format(i[2]) + "\n")
	else:
		print("File: ",inputfile, " does not exist. Please put the LAMMPS file in the correct location.")

