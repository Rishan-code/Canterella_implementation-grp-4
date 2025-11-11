# Canterella_implementation-grp-4

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![LAMMPS](https://img.shields.io/badge/LAMMPS-Simulation-orange)
![MPI](https://img.shields.io/badge/Parallel-MPI-green)
![Status](https://img.shields.io/badge/Build-Passed-success)

## How to Run the Simulation

### Prerequisites
- A working installation of(https://www.lammps.org/) compiled with the `MOLECULE` package.
- Pls install all the reqquirements through the requirements.txt file in the rep
- An MPI implementation for parallel execution (e.g., OpenMPI).
- Clusters would be preferred to run the .sh file in this.

### Steps
1.  Clone this repository:
    ```bash
    git clone https://github.com/Rishan-code/Canterella_implementation-grp-4.git(https://github.com/Rishan-code/Canterella_implementation-grp-4.git)
    ```
2.  Navigate to the simulation directory:
    ```bash
    cd Canterella_implementation/Src
    ```
3.  Generate the LAMMPS data by running the launch.py :
    ```bash
    python launch.py
    ```
4.  Submit the simulation job to a cluster using the provided script (or run locally):
    ```bash
    sbatch run_simulation.sh
    # For local execution (if LAMMPS is in your PATH):
    # mpirun -np 4 lmp -in in.polymer
    ```
## 📊 Results Summary
| Quantity | Analytical (Theory) | Simulation (Mean ± SE) | 95% CI | Deviation |
|-----------|--------------------|------------------------|--------|-----------|
| ⟨Rg²⟩ (Shape) | — | ≈ 28.9 ± 0.07 | [28.7, 29.1] | — |
| ⟨Rg²⟩ (Tree) | — | ≈ 55.0 ± 0.9 | [53.3, 56.7] | — |
| **g-factor (Shape/Tree)** | **0.56 (expected)** | **0.53 ± 0.02** | [0.50, 0.56] | **Δ ≈ 0.03** |

### 🖥️ Example Run Output
```bash
$ python generate_shape_data.py
Parsing 'basic.data'...
Augmenting structure...
```

## Contributors
-(https://github.com/your-username)
- [Saiteja Vemula](https://github.com/username2)
- [Om Shukla](https://github.com/username3)
- [Nimai Gaba](...)
- [Tanishka Shinde](...)

## Acknowledgments
This project was completed as part of the ChE-209 course at Indian Institute Of Technology Indore, instructed by Kailasham. We thank the authors of the original paper, J. Cantarella, T. Deguchi, C. Shonkwiler, and E. Uehara, for their foundational work.

