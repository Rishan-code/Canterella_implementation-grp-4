#!/bin/bash
#SBATCH --job-name=polymer_sim
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4         # number of MPI processes (4 cores)
#SBATCH --time=02:00:00             # walltime (2 hours)
#SBATCH --output=polymer_sim.out    # optional: write output to file
#SBATCH --partition=phd_student
#SBATCH --error=polymer_sim.err     # optional: write errors to file

echo "=== Polymer simulation started on $(date) ==="
echo "Running on host: $(hostname)"
echo "Using $SLURM_NTASKS MPI tasks"

# --- Load LAMMPS module ---
module purge
module load lammps-openmpi                # adjust if your cluster uses a different module name (e.g. lammps/2023 or lammps-mpi)

# --- Run LAMMPS ---
mpirun -np $SLURM_NTASKS lmp -in in.polymer

echo "=== Simulation finished on $(date) ==="
