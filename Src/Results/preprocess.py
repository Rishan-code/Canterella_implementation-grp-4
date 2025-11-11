#!/usr/bin/env python3
import numpy as np
from math import sqrt
import sys

def read_rg2(fname):
    """Read Rg² data from file, ignoring comments."""
    data = []
    with open(fname, 'r') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            parts = s.split()
            # Make sure the line has at least 2 numeric values (TimeStep, v_Rg2)
            if len(parts) >= 2:
                try:
                    data.append(float(parts[1]))  # read second column
                except ValueError:
                    continue
    return np.array(data, dtype=float)

def bootstrap_mean_confidence(data, nboot=2000, ci=95, rng=None):
    rng = np.random.default_rng(rng)
    n = len(data)
    boots = rng.choice(data, size=(nboot, n), replace=True)
    means = boots.mean(axis=1)
    lower = np.percentile(means, (100-ci)/2)
    upper = np.percentile(means, 100 - (100-ci)/2)
    return means.mean(), means.std(ddof=1), (lower, upper), means

def ratio_and_error(meanA, seA, meanB, seB):
    # ratio g = meanA / meanB
    g = meanA / meanB
    # propagate relative errors (assume independent)
    rel_err = sqrt((seA/meanA)**2 + (seB/meanB)**2)
    se_g = g * rel_err
    return g, se_g

def bootstrap_ratio(dataA, dataB, nboot=2000, rng=None):
    rng = np.random.default_rng(rng)
    nA = len(dataA)
    nB = len(dataB)
    boots = []
    for _ in range(nboot):
        sA = rng.choice(dataA, size=nA, replace=True)
        sB = rng.choice(dataB, size=nB, replace=True)
        meanA = sA.mean()
        meanB = sB.mean()
        boots.append(meanA / meanB)
    boots = np.array(boots)
    return boots.mean(), boots.std(ddof=1), np.percentile(boots, [2.5, 97.5]), boots

def main(shape_file="avg_Rg2_shape.dat", tree_file="avg_Rg2_tree.dat", nboot=5000):
    A = read_rg2(shape_file)
    B = read_rg2(tree_file)

    if len(A) < 3 or len(B) < 3:
        print("Error: need at least 3 samples in each file to get reliable stats.")
        return

    # basic stats
    meanA = A.mean(); stdA = A.std(ddof=1); seA = stdA / sqrt(len(A))
    meanB = B.mean(); stdB = B.std(ddof=1); seB = stdB / sqrt(len(B))

    print("=== Basic statistics ===")
    print(f"Shape   : N={len(A)}, mean Rg2 = {meanA:.6f}, std = {stdA:.6f}, SE = {seA:.6f}")
    print(f"Tree    : N={len(B)}, mean Rg2 = {meanB:.6f}, std = {stdB:.6f}, SE = {seB:.6f}")

    # bootstrap mean CI
    meanA_b, std_meanA_b, (lowA, highA), _ = bootstrap_mean_confidence(A, nboot=nboot, rng=42)
    meanB_b, std_meanB_b, (lowB, highB), _ = bootstrap_mean_confidence(B, nboot=nboot, rng=43)
    print("\n=== Bootstrap mean (approx) ===")
    print(f"Shape mean bootstrap mean={meanA_b:.6f}, std_of_means={std_meanA_b:.6f}, 95% CI = [{lowA:.6f}, {highA:.6f}]")
    print(f"Tree  mean bootstrap mean={meanB_b:.6f}, std_of_means={std_meanB_b:.6f}, 95% CI = [{lowB:.6f}, {highB:.6f}]")

    # ratio and propagated error (using SE)
    g, se_g = ratio_and_error(meanA, seA, meanB, seB)
    print("\n=== Ratio g (propagated error) ===")
    print(f"g = {g:.6f} ± {se_g:.6f}  (1σ propagated using independent SEs)")

    # bootstrap ratio
    g_b_mean, g_b_std, g_b_ci, boots = bootstrap_ratio(A, B, nboot=nboot, rng=101)
    print("\n=== Bootstrap ratio g ===")
    print(f"bootstrap mean g = {g_b_mean:.6f}, std = {g_b_std:.6f}, 95% CI = [{g_b_ci[0]:.6f}, {g_b_ci[1]:.6f}]")

    # Save a small report
    with open("rg2_g_report.txt", "w") as f:
        f.write("RG2 & g-factor report\n")
        f.write("======================\n")
        f.write(f"Shape file: {shape_file}\n")
        f.write(f"Tree  file: {tree_file}\n\n")
        f.write(f"Shape: N={len(A)}, mean={meanA:.6f}, std={stdA:.6f}, SE={seA:.6f}\n")
        f.write(f"Tree : N={len(B)}, mean={meanB:.6f}, std={stdB:.6f}, SE={seB:.6f}\n\n")
        f.write(f"g (propagated) = {g:.6f} ± {se_g:.6f}\n")
        f.write(f"g (bootstrap) mean={g_b_mean:.6f}, 95% CI = [{g_b_ci[0]:.6f}, {g_b_ci[1]:.6f}]\n")
    print("\nReport written to rg2_g_report.txt")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main()
