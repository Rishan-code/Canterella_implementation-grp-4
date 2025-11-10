#!/bin/bash
#SBATCH --job-name=polymer_sim_linear
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=00:30:00
#SBATCH --partition=phd_student
#SBATCH --output=polymer_sim_linear.out
#SBATCH --error=polymer_sim_linear.err

# --------------------- LOAD MODULES ---------------------
module purge
module load gnu/8.3.0 openmpi/4.0.2
module load lammps-openmpi

echo "=== Linear Polymer Simulation Started ==="
date

# --------------------- RUN LAMMPS ---------------------
mpirun --oversubscribe -np 8 lmp -in in.linear.lammps

# --------------------- FINISH ---------------------
echo "=== Linear Polymer Simulation Finished ==="
date