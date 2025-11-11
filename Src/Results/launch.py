#!/usr/bin/env python3
"""
Master Result Script
====================
Runs all analysis steps for polymer Rg² comparison between Shape and Tree.
Generates final comparison between analytical and simulation results.
"""

import subprocess
import os
import re
import sys

# === Configuration ===
SHAPE_FILE = "avg_Rg2_shape.dat"
TREE_FILE = "avg_Rg2_tree.dat"
PREPROCESS_SCRIPT = "preprocess.py"
ANALYTICAL_G = 0.582  # from paper/theoretical proof
REPORT_FILE = "../final_results_summary.txt"

def run_preprocess():
    """Runs the preprocessing script to calculate g from simulation data."""
    print("\n🔹 Running preprocessing script...\n")
    try:
        subprocess.run([sys.executable, PREPROCESS_SCRIPT, SHAPE_FILE, TREE_FILE], check=True)
    except subprocess.CalledProcessError:
        print("Error: Preprocessing script failed.")
        sys.exit(1)
    print("Preprocessing completed successfully.\n")

def extract_simulation_g(report_path="rg2_g_report.txt"):
    """Extracts the simulation g-factor from the report file."""
    if not os.path.exists(report_path):
        print(f"Report file '{report_path}' not found.")
        sys.exit(1)

    with open(report_path, "r") as f:
        text = f.read()

    # Use regex to extract g (bootstrap mean)
    match = re.search(r"g \(bootstrap\).*?mean=([\d\.]+).*?\[([\d\.]+), ([\d\.]+)\]", text)
    if match:
        g_sim = float(match.group(1))
        g_low = float(match.group(2))
        g_high = float(match.group(3))
        return g_sim, g_low, g_high
    else:
        print("Could not extract g value from report.")
        return None, None, None

def compare_results(g_sim, g_low, g_high, analytical_g):
    """Compare simulation vs analytical g."""
    diff = abs(g_sim - analytical_g)
    print("=== Final Comparison ===")
    print(f"Analytical g (theory): {analytical_g:.3f}")
    print(f"Simulation g (mean):   {g_sim:.3f}")
    print(f"Simulation 95% CI:     [{g_low:.3f}, {g_high:.3f}]")
    print(f"Absolute difference:   {diff:.3f}\n")

    # Write to file
    with open(REPORT_FILE, "w") as f:
        f.write("=== Final Results Summary ===\n\n")
        f.write(f"Analytical g (theory): {analytical_g:.3f}\n")
        f.write(f"Simulation g (mean):   {g_sim:.3f}\n")
        f.write(f"Simulation 95% CI:     [{g_low:.3f}, {g_high:.3f}]\n")
        f.write(f"Absolute difference:   {diff:.3f}\n")
    print(f"Summary written to {REPORT_FILE}")

def main():
    print("=== Polymer Shape vs Tree Simulation Analysis ===")
    print("=================================================\n")

    # Step 1: Run preprocessing
    run_preprocess()

    # Step 2: Extract simulation g-factor
    g_sim, g_low, g_high = extract_simulation_g()

    if g_sim is None:
        print("Could not extract g value. Exiting.")
        return

    # Step 3: Compare with analytical value
    compare_results(g_sim, g_low, g_high, ANALYTICAL_G)

if __name__ == "__main__":
    main()
