#!/bin/bash
# Name of the job
#SBATCH --job-name=cSiaSiMD

# Submission details
#SBATCH --qos=debug
#SBATCH --constraint=knl
#SBATCH --time=10
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=8
#SBATCH --mem=87G   #Not enough for 64 tasks. Maximum number of tasks per node is 55
# SBATCH -t 2-00:00                      # Runtime in D-HH:MM format

# Outputs
#SBATCH -o 'outputs/cSiaSiMD-%j.output' #File to which STDOUT will be written
#SBATCH --mail-user="dgunruh@ucdavis.edu"
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# allocate the openMP threads
export OMP_PROC_BIND=true
export OMP_PLACES=threads
export OMP_NUM_THREADS=1
export j=$SLURM_JOB_ID

# module swap PrgEnv-intel PrgEnv-gnu
# module load lammps
# module load python3/3.6.0
# module load openmpi

# assign the random seed and the output files for the lammps scripts
s=$j
dumpA=aSi-GAP-$j.xyz
dumpsnapA=aSiBox-GAP-$j.xyz

srun --cpu_bind=cores /global/common/software/m3634/lammps_3Mar2020/gnubuild_KNL/lmp_gnu_knl -var s $s -var d $dumpA -var ds $dumpsnapA -in createAmorphousSi.in
