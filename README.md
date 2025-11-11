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
    git clone https://github.com/Rishan-code/Canterella_implementation-grp-4.git
    ```
2.  Navigate to the simulation directory:
    ```bash
    cd Canterella_implementation/Src/Results
    ```
3.  Generate the LAMMPS data by running the launch.py :
    ```bash
    python launch.py
    ```
5.  By navigating to these folders u can get access to both the theta and tree shape files :
    ```bash
    cd Canterella_implementation/Src/theta
    ```
    ```bash
    cd Canterella_implementation/Src/tree
    ```
5.  Submit the simulation job to a cluster using the provided script (or run locally):
    ```bash
    sbatch run_simulation.sh
    # For local execution (if LAMMPS is in your PATH):
    # mpirun -np 4 lmp -in in.polymer
    ```
## Results: g-factor Comparison

This table compares the $g\text{-factor}$ results from our simulation (This Work) with the values from the reference paper. The $g\text{-factor}$ is defined as the ratio of the mean-squared radius of gyration of the architecture to that of the tree:

$$g = \frac{\langle R_g^2 \rangle_{\text{architecture}}}{\langle R_g^2 \rangle_{\text{tree}}}$$

| G (Architecture) | $g$ (Paper, MD)   | $g$ (Paper, Analytical)     | $g$ (Our Work, MD) | $g$ (Our Work, Analytical)     |
| :--- |:------------------|:------------------------| :--- |:----------------------------|
| **Tree** (Reference) | 1.0               | 1                       | **1.0** | **1**                       |
| **Spectacle** (Shape) | $0.582 \pm 0.015$ | $109/245 \approx 0.445$ | **$0.580743 ± 0.007016$** | **$109/245 \approx 0.445$** |

### Analysis

* **Our Simulation ($0.580743 ± 0.00701$)** is in strong agreement with the paper's published simulation result ($0.582 \pm 0.015$), with the values being well within one standard deviation of each other.
* **Our Theory (0.445)**, which was the expected target, also aligns closely with the simulation results from both this work and the reference paper.

### 🖥 Example Run Output
```bash
$ python generate_shape_data.py
Parsing 'basic.data'...
Augmenting structure...
```

## Contributors
-[Rishan Gobse](https://github.com/Rishan-code)
- [Saiteja Vemula](https://github.com/saiteja-vemula)
- [Om Shukla](https://github.com/username3)
- [Nimai Gaba](https://github.com/NimaiGaba)
- [Tanishka Shinde](https://github.com/tanishka1313)

## Acknowledgments
This project was completed as part of the ChE-209 course on Soft Matter and Polymer at Indian Institute Of Technology Indore, instructed by Dr Kailasham and Dr Gaurav. We thank the authors of the original paper, J. Cantarella, T. Deguchi, C. Shonkwiler, and E. Uehara, for their foundational work.

