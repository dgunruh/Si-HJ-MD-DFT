#!/bin/bash -l

# run one thread for each one the user asks the queue for
# hostname is just for debugging
# hostname
# export OMP_NUM_THREADS=$SLURM_NTASKS
t=13
j=1400
# module load lammps

# the main job executable to run: note the use of srun before it
# srun lmp_serial -in cSiaSi_workingVersion.in
# mpirun lmp_mpi -in cSiaSi_workingVersion.in

# assign the random seed and the output files for the lammps scripts
s=107223+$t
dumpA=aSi-$j-$t.xyz
dumpsnapA=aSiBox-$j-$t.xyz
dumpI=cSiaSiInterface-$j-$t.xyz
dumpsnapI=cSiaSiInterfaceSnapshot-$j-$t.xyz
timestep=$(head -2 aSiBox-$j-$t.xyz | tail -1)

mpirun -np 4 lmp_daily -var s $s -var d $dumpI -var dA $dumpsnapA -var ds $dumpsnapI -var t $timestep -in mergeAmorphousCrystalline.in
