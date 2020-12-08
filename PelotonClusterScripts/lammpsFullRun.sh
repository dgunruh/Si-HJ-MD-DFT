#!/bin/bash -l

# run one thread for each one the user asks the queue for
# hostname is just for debugging
# hostname
# export OMP_NUM_THREADS=$SLURM_NTASKS
t=0
j=100
# module load lammps

# the main job executable to run: note the use of srun before it
# srun lmp_serial -in cSiaSi_workingVersion.in
# mpirun lmp_mpi -in cSiaSi_workingVersion.in

# assign the random seed and the output files for the lammps scripts
s=14223+$t
dumpA=aSi-$j-$t.xyz
dumpsnapA=aSiBox-$j-$t.xyz
dumpI=cSiaSiInterface-$j-$t.xyz
dumpsnapI=cSiaSiInterfaceSnapshot-$j-$t.xyz

# mpirun -np 8 lmp_daily -var s $s -var d $dumpA -var ds $dumpsnapA -in createAmorphousSi.in
# python3 trimBox.py $t $j
mpirun -np 4 lmp_daily -var s $s -var d $dumpI -var dA $dumpsnapA -var ds $dumpsnapI -in mergeAmorphousCrystalline.in
