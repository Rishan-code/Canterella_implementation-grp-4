#!/bin/bash
#SBATCH --job-name=polymer_sim
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1            # 8 MPI tasks (adjust if needed)
#SBATCH --time=00:30:00                # 2 hours walltime
#SBATCH --partition=phd_student
#SBATCH --output=polymer_sim.out       # Std output file
#SBATCH --error=polymer_sim.err        # Std error file

# --------------------- LOAD MODULES ---------------------
module purge
module load gnu/8.3.0 openmpi/4.0.2
module load lammps-openmpi

# --------------------- NAVIGATE TO SRC ---------------------
cd ~/Canterella_implementation-grp-4/Src

echo "=== Polymer Simulation Started on $(hostname) ==="
date

# --------------------- RUN LAMMPS ---------------------
mpirun --oversubscribe -np 8 lmp -in in.lammps

# --------------------- FINISH ---------------------
echo "=== Polymer Simulation Finished ==="
date