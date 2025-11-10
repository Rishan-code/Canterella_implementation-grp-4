#!/bin/bash
#SBATCH --job-name=tree_sim
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --partition=phd_student
#SBATCH --output=tree.out
#SBATCH --error=tree.err

module purge
module load gcc-11.5
module load openmpi-4.1.5
module load lammps-openmpi

echo "=== Tree Polymer Simulation Started on $(hostname) ==="
date

# ✅ Explicit LAMMPS path avoids ambiguity
mpirun -np $SLURM_NTASKS /apps/codes/lammps-29Aug2024/bin/lmp -in tree_in.lammps

echo "=== Tree Polymer Simulation Finished ==="
date

