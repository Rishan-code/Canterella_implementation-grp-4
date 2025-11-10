#!/bin/bash
#SBATCH --job-name=spectacle_sim
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8            # 8 MPI tasks (adjust as needed)
#SBATCH --time=00:45:00                # 45 minutes walltime
#SBATCH --partition=phd_student
#SBATCH --output=spectacle_sim.out     # Std output file
#SBATCH --error=spectacle_sim.err      # Std error file

# --------------------- LOAD MODULES ---------------------
module purge
module load gnu/8.3.0 openmpi/4.0.2
module load lammps-openmpi

echo "=== Spectacle Polymer Simulation Started on $(hostname) ==="
date
echo "Running on $SLURM_NTASKS cores"

# --------------------- RUN LAMMPS ---------------------
mpirun --oversubscribe -np $SLURM_NTASKS lmp -in in.spectacle.lammps

# --------------------- FINISH ---------------------
echo "=== Spectacle Polymer Simulation Finished ==="
date
