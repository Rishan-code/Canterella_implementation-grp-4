# Canterella_implementation-grp-4
## How to Run the Simulation

### Prerequisites
- A working installation of(https://www.lammps.org/) compiled with the `MOLECULE` package.
- [Moltemplate](https://www.moltemplate.org/) for building the system topology.
- An MPI implementation for parallel execution (e.g., OpenMPI).

### Steps
1.  Clone this repository:
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    ```
2.  Navigate to the simulation directory:
    ```bash
    cd your-repo-name/simulation/
    ```
3.  Generate the LAMMPS data file using Moltemplate:
    ```bash
    moltemplate.sh moltemplate_files/system.lt
    ```
4.  Submit the simulation job to a cluster using the provided script (or run locally):
    ```bash
    sbatch run_simulation.sh
    # For local execution (if LAMMPS is in your PATH):
    # mpirun -np 4 lmp -in in.polymer
    ```

## Results Summary

This table compares our calculated values with the target values from the reference paper.

| Quantity | Paper Target | Analytical Result | Simulation Result |
| :--- | :---: | :---: | :---: |
| $g(G_\infty)$ | $109/405 \approx 0.269$ | $361/1620 \approx 0.223$ | N/A |
| $\langle R_g^2 \rangle^{1/2}$ (LJ units) | $\approx 2.45$ | N/A | *[Enter your value here]* |

*Note: The analytical result for g-factor is derived using the formula and eigenvalues provided in the reference paper. The discrepancy between our result and the paper's stated result is due to a numerical error in the source text's final calculation.*

## Contributors
-(https://github.com/your-username)
- [Group Member 2](https://github.com/username2)
- [Group Member 3](https://github.com/username3)

## Acknowledgments
This project was completed as part of the [Course Name] course at [University Name], instructed by [Professor's Name]. We thank the authors of the original paper, J. Cantarella, T. Deguchi, C. Shonkwiler, and E. Uehara, for their foundational work.