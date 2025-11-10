import sys

# --- Configuration ---
NUM_ATOMS = 10  # This creates 9 bonds and 8 angles
BOND_DIST = 1.5 # Equilibrium bond length from your in.lammps file
FILENAME = "linear.data"
# ---------------------

print(f"Generating LAMMPS data file for a linear polymer...")
print(f"  Atoms: {NUM_ATOMS}")
print(f"  Bonds: {NUM_ATOMS - 1}")
print(f"  Angles: {NUM_ATOMS - 2}")

try:
    with open(FILENAME, 'w') as f:
        f.write("LAMMPS data file - Linear Polymer (N=10)\n\n")

        # --- Header ---
        f.write(f"{NUM_ATOMS} atoms\n")
        f.write(f"{NUM_ATOMS - 1} bonds\n")
        f.write(f"{NUM_ATOMS - 2} angles\n\n")

        f.write("1 atom types\n")
        f.write("1 bond types\n")
        f.write("1 angle types\n\n")

        # --- Box Dimensions (same as your working sim) ---
        f.write("-20.00 20.00 xlo xhi\n")
        f.write("-20.00 20.00 ylo yhi\n")
        f.write("-20.00 20.00 zlo zhi\n\n")

        # --- Masses ---
        f.write("Masses\n\n")
        f.write("1 12.011\n\n")

        # --- Atoms ---
        # We will create a simple straight line of atoms
        f.write("Atoms # atomic\n\n")
        for i in range(1, NUM_ATOMS + 1):
            atom_id = i
            mol_id = 1
            atom_type = 1
            x = (i - 1) * BOND_DIST
            y = 0.0
            z = 0.0
            f.write(f"{atom_id} {mol_id} {atom_type} {x:.4f} {y:.4f} {z:.4f}\n")

        # --- Bonds ---
        f.write("\nBonds # bond\n\n")
        for i in range(1, NUM_ATOMS):
            bond_id = i
            bond_type = 1
            atom1 = i
            atom2 = i + 1
            f.write(f"{bond_id} {bond_type} {atom1} {atom2}\n")

        # --- Angles ---
        f.write("\nAngles\n\n")
        for i in range(1, NUM_ATOMS - 1):
            angle_id = i
            angle_type = 1
            atom1 = i
            atom2 = i + 1
            atom3 = i + 2
            f.write(f"{angle_id} {angle_type} {atom1} {atom2} {atom3}\n")

    print(f"\nSuccess! Created file: {FILENAME}")

except Exception as e:
    print(f"An error occurred: {e}")