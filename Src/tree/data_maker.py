#!/usr/bin/env python3
import numpy as np

# ---------------- CONFIGURATION ----------------
output_file = "data.tree_equalized.lammps"

# target: ~96 atoms total (same as spectacle shape)
main_branch_length = 10        # beads from center to each Y junction
sub_branch_length = 11         # beads per Y arm
main_angle_deg = 120           # angle between main branches
sub_angle_deg = 45             # sub-branch split angle
bond_length = 1.0              # inter-bead spacing
mass_all = 1.0                 # equal mass for all atoms
# ------------------------------------------------


def rotation_matrix_z(theta_deg):
    """Rotation matrix for rotation about z-axis."""
    t = np.deg2rad(theta_deg)
    return np.array([
        [np.cos(t), -np.sin(t), 0],
        [np.sin(t),  np.cos(t), 0],
        [0, 0, 1]
    ])


def generate_triple_Y():
    """Generate 3 Y-shaped branches joined at the center."""
    atoms = []
    bonds = []
    atom_id = 1
    bond_id = 1

    # central atom
    atoms.append((atom_id, 1, 1, 0.0, 0.0, 0.0))
    center_id = atom_id

    for main_i in range(3):
        angle_main = main_i * main_angle_deg
        R_main = rotation_matrix_z(angle_main)
        main_dir = R_main @ np.array([1.0, 0.0, 0.0])

        prev = center_id
        main_ids = []

        # main branch
        for i in range(1, main_branch_length + 1):
            atom_id += 1
            pos = main_dir * bond_length * i
            atoms.append((atom_id, 1, 2, *pos))
            bonds.append((bond_id, 1, prev, atom_id))
            prev = atom_id
            bond_id += 1
            main_ids.append(atom_id)

        # sub-branches at tip
        tip_pos = main_dir * bond_length * main_branch_length
        tip_id = main_ids[-1]
        for sign in [+1, -1]:
            R_sub = rotation_matrix_z(sign * sub_angle_deg)
            sub_dir = R_sub @ main_dir
            prev = tip_id
            for j in range(1, sub_branch_length + 1):
                atom_id += 1
                pos = tip_pos + sub_dir * bond_length * j
                atoms.append((atom_id, 1, 2, *pos))
                bonds.append((bond_id, 1, prev, atom_id))
                prev = atom_id
                bond_id += 1

    return atoms, bonds


def write_lammps_data(filename, atoms, bonds, mass):
    """Write LAMMPS-compatible data file."""
    with open(filename, "w") as f:
        f.write("LAMMPS data file - Tree polymer (mass=1, equalized)\n\n")
        f.write(f"{len(atoms)} atoms\n{len(bonds)} bonds\n0 angles\n\n")
        f.write("2 atom types\n1 bond types\n\n")

        coords = np.array([a[3:] for a in atoms])
        margin = 2.0
        xmin, ymin, zmin = coords.min(axis=0) - margin
        xmax, ymax, zmax = coords.max(axis=0) + margin
        f.write(f"{xmin:.3f} {xmax:.3f} xlo xhi\n")
        f.write(f"{ymin:.3f} {ymax:.3f} ylo yhi\n")
        f.write(f"{zmin:.3f} {zmax:.3f} zlo zhi\n\n")

        # masses
        f.write("Masses\n\n")
        f.write(f"1 {mass:.3f}\n2 {mass:.3f}\n\n")

        # atoms
        f.write("Atoms # atomic\n\n")
        for a in atoms:
            f.write(f"{a[0]} {a[1]} {a[2]} {a[3]:.6f} {a[4]:.6f} {a[5]:.6f}\n")

        # bonds
        f.write("\nBonds # bond\n\n")
        for b in bonds:
            f.write(f"{b[0]} {b[1]} {b[2]} {b[3]}\n")

    print(f"✅ '{filename}' written with {len(atoms)} atoms, {len(bonds)} bonds, all masses={mass}")


if __name__ == "__main__":
    atoms, bonds = generate_triple_Y()
    write_lammps_data(output_file, atoms, bonds, mass_all)
