#!/usr/bin/env python3
import numpy as np
import sys
from collections import defaultdict

# --- Configuration ---
original_data_file = 'basic.data'            # input file
augmented_data_file = 'data.spectacle.lammps'  # output file
dummy_atoms_per_bond = 10  # beads per bond
arc_height = 1.5  # base curvature height
# --- End Configuration ---


def parse_lammps_data(filename):
    """Simple parser for LAMMPS data file"""
    data = {
        'atoms': [],
        'bonds': [],
        'angles': [],
        'headers': {
            'atoms': 0, 'bonds': 0, 'angles': 0,
            'atom types': 0, 'bond types': 0, 'angle types': 0,
            'x': None, 'y': None, 'z': None
        }
    }

    section = None
    try:
        with open(filename, 'r') as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                tokens = line.split()

                # --- headers ---
                if len(tokens) >= 2 and tokens[1] in ('atoms', 'bonds', 'angles'):
                    try:
                        count = int(tokens[0])
                        data['headers'][tokens[1]] = count
                    except: pass
                    continue

                if 'atom types' in line:
                    data['headers']['atom types'] = int(tokens[0])
                    continue
                if 'bond types' in line:
                    data['headers']['bond types'] = int(tokens[0])
                    continue

                if 'xlo' in line and 'xhi' in line:
                    data['headers']['x'] = (float(tokens[0]), float(tokens[1]))
                    continue
                if 'ylo' in line and 'yhi' in line:
                    data['headers']['y'] = (float(tokens[0]), float(tokens[1]))
                    continue
                if 'zlo' in line and 'zhi' in line:
                    data['headers']['z'] = (float(tokens[0]), float(tokens[1]))
                    continue

                # --- detect section ---
                if tokens[0].lower().startswith('atoms'):
                    section = 'atoms'; continue
                if tokens[0].lower().startswith('bonds'):
                    section = 'bonds'; continue
                if tokens[0].lower().startswith('angles'):
                    section = 'angles'; continue

                # --- read sections ---
                if section == 'atoms':
                    if len(tokens) >= 6:
                        atom_id, mol_id, atom_type = int(tokens[0]), int(tokens[1]), int(tokens[2])
                        x, y, z = float(tokens[3]), float(tokens[4]), float(tokens[5])
                    elif len(tokens) >= 5:
                        atom_id, mol_id, atom_type = int(tokens[0]), 1, int(tokens[1])
                        x, y, z = float(tokens[2]), float(tokens[3]), float(tokens[4])
                    else:
                        continue
                    data['atoms'].append({'id': atom_id, 'mol': mol_id, 'type': atom_type,
                                          'pos': np.array([x, y, z], dtype=float)})
                elif section == 'bonds':
                    if len(tokens) >= 4:
                        bid, btype, a1, a2 = int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])
                        data['bonds'].append({'id': bid, 'type': btype, 'a1': a1, 'a2': a2})

        if data['headers']['bond types'] == 0:
            data['headers']['bond types'] = 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading data: {e}")
        sys.exit(1)

    return data


def generate_arc_points(p1, p2, h_start, h_end, n, out_vector):
    """Generate N dummy points along an arc varying from h_start to h_end."""
    if n <= 0:
        return []
    out = np.array(out_vector, dtype=float)
    out /= np.linalg.norm(out) if np.linalg.norm(out) else 1.0
    v = p2 - p1
    points = []
    for i in range(1, n + 1):
        t = i / (n + 1.0)
        h_t = h_start + (h_end - h_start) * t
        p_linear = p1 + t * v
        p_curved = h_t * np.sin(np.pi * t) * out
        points.append(p_linear + p_curved)
    return points


def augment_data(data, N, h):
    """Add dummy atoms forming smooth arcs for visualization."""
    original_atoms = data['atoms']
    original_bonds = data['bonds']
    atom_pos_map = {a['id']: a['pos'] for a in original_atoms}

    new_atoms, new_bonds = [], []
    for atom in original_atoms:
        new_atoms.append({'id': atom['id'], 'mol': 1, 'type': 1, 'pos': np.array(atom['pos'], dtype=float)})

    current_atom_id = max(a['id'] for a in new_atoms)
    current_bond_id = max(b['id'] for b in original_bonds) if original_bonds else 0
    bond_heights = defaultdict(lambda: h)

    for bond in original_bonds:
        a1_orig, a2_orig = bond['a1'], bond['a2']
        a1, a2 = sorted((a1_orig, a2_orig))

        # --- Determine curvature direction ---
        if (a1, a2) == (3, 4):
            out_vector = np.array([0.0, 0.0, 0.0])  # straight bridge
        elif (a1, a2) in [(1, 2), (5, 6)]:
            out_vector = np.array([1.0, 0.0, 0.0])  # loops → X
        else:
            y_mid = (atom_pos_map[a1_orig][1] + atom_pos_map[a2_orig][1]) / 2.0
            out_vector = np.array([0.0, 1.0, 0.0]) if y_mid >= 0 else np.array([0.0, -1.0, 0.0])

        # --- Curvature scaling ---
        current_h = bond_heights[(a1, a2)]
        if (a1, a2) in [(1, 2), (5, 6)]:  # outer loops
            current_h *= 1.5
        elif (a1, a2) in [(2, 3), (4, 5)]:  # inner loops
            current_h *= 0.7
        elif (a1, a2) == (3, 4):
            current_h = 0.0
        bond_heights[(a1, a2)] *= -1

        p1, p2 = atom_pos_map[a1_orig], atom_pos_map[a2_orig]

        # --- Asymmetric curvature for loops ---
        if (a1, a2) == (1, 2):
            h_start, h_end = current_h * 0.3, current_h * 0.7
        elif (a1, a2) == (5, 6):
            h_start, h_end = current_h * 0.7, current_h * 0.3
        else:
            h_start = h_end = current_h

        dummy_coords = generate_arc_points(p1, p2, h_start, h_end, N, out_vector)

        # Add new dummy atoms
        dummy_ids = []
        for pos in dummy_coords:
            current_atom_id += 1
            dummy_ids.append(current_atom_id)
            new_atoms.append({'id': current_atom_id, 'mol': 1, 'type': 2, 'pos': pos})

        # Add bonds connecting all atoms in sequence
        chain_atoms = [a1_orig] + dummy_ids + [a2_orig]
        for i in range(len(chain_atoms) - 1):
            current_bond_id += 1
            new_bonds.append({'id': current_bond_id, 'type': 1,
                              'a1': chain_atoms[i], 'a2': chain_atoms[i + 1]})

    return new_atoms, new_bonds


def write_augmented_data(filename, atoms, bonds, headers):
    """Write new augmented data file."""
    total_atoms, total_bonds = len(atoms), len(bonds)
    with open(filename, 'w') as f:
        f.write(f"LAMMPS data file - Spectacle (N={dummy_atoms_per_bond})\n\n")
        f.write(f"{total_atoms} atoms\n{total_bonds} bonds\n0 angles\n\n")
        f.write(f"2 atom types\n{headers.get('bond types',1)} bond types\n\n")

        all_pos = np.array([a['pos'] for a in atoms])
        xlo, xhi = np.min(all_pos[:,0])-2, np.max(all_pos[:,0])+2
        ylo, yhi = np.min(all_pos[:,1])-2, np.max(all_pos[:,1])+2
        zlo, zhi = np.min(all_pos[:,2])-2, np.max(all_pos[:,2])+2
        f.write(f"{xlo:.4f} {xhi:.4f} xlo xhi\n{ylo:.4f} {yhi:.4f} ylo yhi\n{zlo:.4f} {zhi:.4f} zlo zhi\n\n")

        f.write("Masses\n\n1 12.011\n2 0.001\n\n")
        f.write("Atoms # atomic\n\n")
        for a in atoms:
            x,y,z = a['pos']
            f.write(f"{a['id']} {a['mol']} {a['type']} {x:.6f} {y:.6f} {z:.6f}\n")
        f.write("\nBonds # bond\n\n")
        for b in bonds:
            f.write(f"{b['id']} {b['type']} {b['a1']} {b['a2']}\n")
    print(f"\n✅ Created '{filename}' with {total_atoms} atoms and {total_bonds} bonds.\n")


# --- Main ---
if __name__ == "__main__":
    print(f"Parsing '{original_data_file}'...")
    data = parse_lammps_data(original_data_file)
    print("Augmenting structure...")
    atoms, bonds = augment_data(data, dummy_atoms_per_bond, arc_height)
    print("Writing output...")
    write_augmented_data(augmented_data_file, atoms, bonds, data['headers'])
