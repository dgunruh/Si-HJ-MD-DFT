NEB in LAMMPS is a multi-replica simulation. This requires LAMMPS to have been built with the REPLICA package. 
To run NEB, you must run with one or more processors per replica. The processors assigned to each replcia are determined at run-time by using the -partition command-line switch to launch LAMMPS on multiple partitions, which in this context are the same as replicas. 
	E.g.: mpirun -np 16 lmp_linux -partition 8x1 -in in.neb runs 8 replicas, on 8 processors. 
	-partition 8x2 runs 8 replicas on 16 processors.
Also, you must define input scripts as -in in.neb rather than < in.neb

LAMMPS recommendations:
	The energy minimizers will try to act on every atom in the system. Therefore, restrict motion using the fix setforce command
	An atom map must be defined, use the atom_modify map command to do this.
	Finally, the timestep for NEB is recommended to be 10x larger than the timestep normally used for dynamics simulations

Final file format:
	The file can contain initial blank lines or comment lines tarting with the "#" which are ignored. 
	the first non-blank, non-comment line should list N = the number of lines to follow.
	The following lines should be formatted as IDN xN yN zN

Useful LAMMPS python scripts:
	In the folder tools/python:
	neb_combine.py
	neb_final.py

Input files:
	Sample input files can be found in the Dropbox, under "NEB Barrier Heights"/09132020/09-13-2020_inputs"

NEB command: neb etol ftol N1 N2 Nevery file-style arg keyword
	etol = stopping tolerance for energy
	ftol = stopping tolerance for force
	N1 = max # of iterations (timesteps) to run initial NEB
	N2 = max # of iterations to run barrier-climbing NEB
	Nevery = print replica energies and reaction coordinates every this many timesteps
	file-style = final or each or none. We want final: file with initial coords for final replica

Paired command: fix neb

