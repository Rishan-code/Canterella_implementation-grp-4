# analyze_rg.py

import matplotlib.pyplot as plt
import numpy as np

def read_rg_data(log_file):
    timesteps = []
    rg_values = []
    with open(log_file, 'r') as f:
        recording = False
        for line in f:
            if 'Step' in line and 'c_RG' in line:
                recording = True
                continue
            if recording:
                if line.strip() == '' or 'Loop time' in line:
                    break
                parts = line.strip().split()
                if len(parts) >= 2:
                    timestep = int(parts[0])
                    rg = float(parts[1])
                    timesteps.append(timestep)
                    rg_values.append(rg)
    return np.array(timesteps), np.array(rg_values)

def main():
    log_file = "theta_graph.out"  # or log.lammps
    timesteps, rg = read_rg_data(log_file)

    avg_rg = np.mean(rg)
    std_rg = np.std(rg)

    print(f"Average Rg: {avg_rg:.4f} ± {std_rg:.4f}")

    plt.figure(figsize=(8, 4))
    plt.plot(timesteps, rg, label='Rg over time')
    plt.axhline(avg_rg, color='r', linestyle='--', label='Mean Rg')
    plt.xlabel('Timestep')
    plt.ylabel('Radius of Gyration')
    plt.title('Rg vs Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig("rg_plot.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
