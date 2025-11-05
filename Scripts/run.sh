#!/bin/bash
#SBATCH --job-name=polymer_sim
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=04:00:00
#SBATCH --partition=phd_student

# Load necessary modules (example for a generic cluster)
module purge
module load gnu/8.3.0 openmpi/4.0.2
module load lammps-openmpi

# Run LAMMPS in parallel
mpirun -np 16 lmp -in in.lammps