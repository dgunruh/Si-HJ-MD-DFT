#!/bin/bash
#
#! -cwd
#! -j y
#! -S /bin/bash

# Name of the job
#SBATCH --job-name=cSiaSiMD
#SBATCH --ntasks=256
#SBATCH --ntasks-per-node=64
#SBATCH -c 1
#SBATCH --mem=140G
#SBATCH --partition=high2                 # Use the med2 partition
#SBATCH -t 2-00:00                      # Runtime in D-HH:MM format
#SBATCH -o 'outputs/cSiaSiMD-%j.output' #File to which STDOUT will be written
#SBATCH --mail-user="dgunruh@ucdavis.edu"
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# run one thread for each one the user asks the queue for
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export j=$SLURM_JOB_ID
module load openmpi

# assign the random seed and the output files for the lammps scripts
s=$j
dumpA=aSi-GAP-$j.xyz
dumpsnapA=aSiBox-GAP-$j.xyz

srun ../src/lammps-stable_3Mar2020/build/lmp_mpi -var s $s -var d $dumpA -var ds $dumpsnapA -in createAmorphousSi.in
