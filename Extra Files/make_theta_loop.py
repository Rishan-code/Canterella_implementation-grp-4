#!/usr/bin/env python3
"""
make_spectacle_N10.py

Generate a θ-shaped "spectacle" polymer topology (two loops + bridge)
in LAMMPS data file format.

Output closely matches the structure:
96 atoms, 99 bonds, 0 angles  (for N=10)
"""

import numpy as np


# ====================== CONFIG ======================
N = 10  # number of beads per half loop (adjust for more resolution)
filename = f"spectacle_N{N}.data"
R_loop = 4.0       # approximate loop radius
bridge_height = 3.0  # distance between upper and lower nodes
mass_main = 12.011
mass_dummy = 0.001
# ====================================================


def generate_arc(center, radius, y_offset, n_points, direction="up"):
    """Generate points for a semicircular arc centered at given center (x0, y0)."""
    x0, y0 = center
    if direction == "up":
        theta = np.linspace(np.pi, 0, n_points)
    else:  # "down"
        theta = np.linspace(0, -np.pi, n_points)

    x = x0 + radius * np.cos(theta)
    y = y0 + y_offset + radius * np.sin(theta)
    return np.column_stack((x, y))


def write_data(filename, atoms, bonds):
    """Write a LAMMPS-style data file."""
    with open(filename, "w") as f:
        f.write(f"LAMMPS data file - Spectacle (N={N})\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write(f"{len(bonds)} bonds\n")
        f.write("0 angles\n\n")
        f.write("2 atom types\n1 bond types\n\n")

        xlo, xhi = -7.1540, 7.1540
        ylo, yhi = -4.7575, 4.7575
        zlo, zhi = -2.0, 2.0
        f.write(f"{xlo:.4f} {xhi:.4f} xlo xhi\n")
        f.write(f"{ylo:.4f} {yhi:.4f} ylo yhi\n")
        f.write(f"{zlo:.4f} {zhi:.4f} zlo zhi\n\n")

        f.write("Masses\n\n")
        f.write(f"1 {mass_main}\n2 {mass_dummy}\n\n")

        f.write("Atoms # atomic\n\n")
        for a in atoms:
            f.write(f"{a['id']} {a['mol']} {a['type']} "
                    f"{a['pos'][0]:.6f} {a['pos'][1]:.6f} {a['pos'][2]:.6f}\n")

        f.write("\nBonds # bond\n\n")
        for b in bonds:
            f.write(f"{b['id']} {b['type']} {b['a1']} {b['a2']}\n")

    print(f"✅ Wrote {filename} ({len(atoms)} atoms, {len(bonds)} bonds)")


def main():
    atoms = []
    bonds = []

    atom_id = 0
    bond_id = 0

    # === Define main anchor nodes ===
    # Left top, left bottom, center top, center bottom, right top, right bottom
    anchors = {
        1: np.array([-R_loop, 1.0, 0.0]),
        2: np.array([-R_loop, -1.0, 0.0]),
        3: np.array([0.0, 1.5, 0.0]),
        4: np.array([0.0, -1.5, 0.0]),
        5: np.array([R_loop, 1.0, 0.0]),
        6: np.array([R_loop, -1.0, 0.0])
    }

    for i, pos in anchors.items():
        atom_id += 1
        atoms.append({'id': i, 'mol': 1, 'type': 1, 'pos': pos})

    # === Left Loop (upper and lower arcs) ===
    left_top = anchors[1]
    left_bottom = anchors[2]
    left_center = ((left_top + left_bottom) / 2)[:2]

    # upper half (1 -> 2)
    arc1 = generate_arc(left_center, 1.0, 0.0, N, direction="up")

    # add atoms along arc
    prev = 1
    for i in range(N):
        atom_id += 1
        atoms.append({'id': atom_id, 'mol': 1, 'type': 2,
                      'pos': np.array([arc1[i, 0], arc1[i, 1], 0.0])})
        bonds.append({'id': bond_id + 1, 'type': 1, 'a1': prev, 'a2': atom_id})
        prev = atom_id
        bond_id += 1
    bonds.append({'id': bond_id + 1, 'type': 1, 'a1': prev, 'a2': 2})
    bond_id += 1

    # === Central bridge ===
    bridge = np.linspace(anchors[3], anchors[4], N)
    prev = 3
    for i in range(1, N - 1):
        atom_id += 1
        atoms.append({'id': atom_id, 'mol': 1, 'type': 2,
                      'pos': bridge[i]})
        bonds.append({'id': bond_id + 1, 'type': 1, 'a1': prev, 'a2': atom_id})
        prev = atom_id
        bond_id += 1
    bonds.append({'id': bond_id + 1, 'type': 1, 'a1': prev, 'a2': 4})
    bond_id += 1

    # === Right loop (mirror of left) ===
    right_top = anchors[5]
    right_bottom = anchors[6]
    right_center = ((right_top + right_bottom) / 2)[:2]
    arc2 = generate_arc(right_center, 1.0, 0.0, N, direction="down")

    prev = 5
    for i in range(N):
        atom_id += 1
        atoms.append({'id': atom_id, 'mol': 1, 'type': 2,
                      'pos': np.array([arc2[i, 0], arc2[i, 1], 0.0])})
        bonds.append({'id': bond_id + 1, 'type': 1, 'a1': prev, 'a2': atom_id})
        prev = atom_id
        bond_id += 1
    bonds.append({'id': bond_id + 1, 'type': 1, 'a1': prev, 'a2': 6})
    bond_id += 1

    # === Connectors (left loop to bridge, bridge to right loop) ===
    connectors = [
        (1, 3), (3, 5),
        (2, 4), (4, 6)
    ]
    for c in connectors:
        bond_id += 1
        bonds.append({'id': bond_id, 'type': 1, 'a1': c[0], 'a2': c[1]})

    write_data(filename, atoms, bonds)


if __name__ == "__main__":
    main()
