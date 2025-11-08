import numpy as np
import sys
from collections import defaultdict

# --- Configuration ---
# Use your original 6-atom file as input
original_data_file = 'basic.data'
augmented_data_file = 'data.curved.lammps'  # Output file
dummy_atoms_per_bond = 10  # N: Number of beads in the chain (N+1 bonds)
arc_height = 1.5  # h: Arc height in Angstroms


# --- End Configuration ---

def parse_lammps_data(filename):
    """Parses your 6-atom LAMMPS data file."""
    data = {'atoms': [], 'bonds': [], 'headers': {}}
    section = None
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # <-- FIX: Must take the first element [0] from the split list
                if line.endswith('atoms'):
                    data['headers']['atoms'] = int(line.split()[0])
                    continue
                if line.endswith('bonds'):
                    data['headers']['bonds'] = int(line.split()[0])
                    continue
                if line.endswith('atom types'):
                    data['headers']['atom types'] = int(line.split()[0])
                    continue
                if line.endswith('bond types'):
                    data['headers']['bond types'] = int(line.split()[0])
                    continue
                if line.endswith('xlo xhi'):
                    data['headers']['x'] = line
                    continue
                if line.endswith('ylo yhi'):
                    data['headers']['y'] = line
                    continue
                if line.endswith('zlo zhi'):
                    data['headers']['z'] = line
                    continue

                if line.startswith('Atoms'):
                    section = 'atoms'
                    continue
                if line.startswith('Bonds'):
                    section = 'bonds'
                    continue
                if line.startswith('Masses'):
                    section = 'masses'
                    continue

                if section == 'atoms':
                    parts = line.split()
                    atom_id = int(parts[0])  # <-- FIX: Was int(parts)
                    atom_type = int(parts[1])
                    pos = np.array([float(x) for x in parts[2:5]])
                    data['atoms'].append({'id': atom_id, 'type': atom_type, 'pos': pos, 'line': line})

                if section == 'bonds':
                    parts = line.split()
                    bond_id = int(parts[0])  # <-- FIX: Was int(parts)
                    bond_type = int(parts[1])
                    a1 = int(parts[2])
                    a2 = int(parts[3])
                    data['bonds'].append({'id': bond_id, 'type': bond_type, 'a1': a1, 'a2': a2})

    except FileNotFoundError:
        print(f"Error: Original data file '{filename}' not found.")
        print(f"Please ensure your data file is named '{original_data_file}' and is in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file: {e} on line: {line}")
        sys.exit(1)

    return data


def generate_arc_points(p1, p2, h, n, out_vector=np.array([1.0, 0.0, 0.0])):
    """
    Generates N intermediate points on an arc.
    MODIFIED: out_vector is now set to the X-direction.
    """
    points = []  # <-- FIX: Was None
    v = p2 - p1
    for i in range(1, n + 1):
        t = i / (n + 1.0)
        p_linear = p1 + t * v
        # Use sine interpolation for a smooth arc
        p_curved = h * np.sin(np.pi * t) * out_vector
        points.append(p_linear + p_curved)
    return points


def augment_data(data, N, h):
    """Augments the data structure with dummy atoms and curved bonds."""

    original_atoms = data['atoms']
    original_bonds = data['bonds']

    atom_pos_map = {a['id']: a['pos'] for a in original_atoms}

    new_atoms_list = []  # <-- FIX: Was None
    new_bonds_list = []  # <-- FIX: Was None

    # Add original atoms, re-typed as Type 1
    for atom in original_atoms:
        atom['type'] = 1  # Set original atoms to type 1
        new_atoms_list.append(atom)

    current_atom_id = len(original_atoms)
    current_bond_id = 0

    bond_counts = defaultdict(int)
    bond_heights = defaultdict(lambda: h)

    for bond in original_bonds:
        a1, a2 = sorted((bond['a1'], bond['a2']))

        # Check if this is one of the parallel bond pairs
        if (a1, a2) in [(1, 2), (5, 6)]:
            bond_counts[(a1, a2)] += 1
            current_h = bond_heights[(a1, a2)]
            bond_heights[(a1, a2)] *= -1  # Flip height for the next parallel bond

            p1 = atom_pos_map[a1]
            p2 = atom_pos_map[a2]

            # 1. Generate N new dummy atom coordinates
            dummy_coords = generate_arc_points(p1, p2, current_h, N)

            # 2. Add N new dummy atoms (Type 2)
            dummy_atom_ids = []  # <-- FIX: Was None
            for pos in dummy_coords:
                current_atom_id += 1
                dummy_atom_ids.append(current_atom_id)
                new_atom = {
                    'id': current_atom_id,
                    'type': 2,  # Set dummy atoms to type 2
                    'pos': pos
                }
                new_atoms_list.append(new_atom)

            # 3. Add N+1 new bonds to form the chain
            chain_atoms = [a1] + dummy_atom_ids + [a2]
            for i in range(len(chain_atoms) - 1):
                current_bond_id += 1
                new_bond = {
                    'id': current_bond_id,
                    'type': 1,  # All bonds are type 1
                    'a1': chain_atoms[i],
                    'a2': chain_atoms[i + 1]
                }
                new_bonds_list.append(new_bond)

        else:
            # This is a single bond; keep it as-is
            current_bond_id += 1
            new_bonds_list.append({
                'id': current_bond_id,
                'type': bond['type'],
                'a1': bond['a1'],
                'a2': bond['a2']
            })

    return new_atoms_list, new_bonds_list


def write_augmented_data(filename, atoms, bonds, headers):
    """Writes the new, augmented LAMMPS data file."""
    with open(filename, 'w') as f:
        f.write(f"LAMMPS data file - Augmented for curved bonds (N={dummy_atoms_per_bond})\n\n")

        f.write(f"{len(atoms)} atoms\n")
        f.write(f"{len(bonds)} bonds\n\n")

        f.write(f"2 atom types\n")  # Type 1 = Original, Type 2 = Dummy
        f.write(f"{headers['bond types']} bond types\n\n")

        # Adjust box bounds to include the new arcs
        x_line = headers['x']
        x_parts = x_line.split()
        xlo = float(x_parts[0])  # <-- FIX: Was float(x_parts)
        xhi = float(x_parts[1])
        f.write(f"{min(xlo, -arc_height) - 1.0:.4f} {max(xhi, arc_height) + 1.0:.4f} xlo xhi\n")

        f.write(f"{headers['y']}\n")
        f.write(f"{headers['z']}\n\n")

        f.write("Masses\n\n")
        f.write("1 12.011\n")  # Mass for Type 1 (Original)
        f.write("2 0.001\n\n")  # Mass for Type 2 (Dummy) - small, non-zero

        f.write("Atoms # atomic\n\n")
        for atom in atoms:
            pos = atom['pos']
            # <-- FIX: Was {pos:.6f}, which fails on an array. Must index [0].
            f.write(f"{atom['id']} {atom['type']} {pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f}\n")

        f.write("\nBonds # bond\n\n")
        for bond in bonds:
            f.write(f"{bond['id']} {bond['type']} {bond['a1']} {bond['a2']}\n")

    # <-- FIX: Made print statements dynamic based on parsed data
    num_original_atoms = headers['atoms']
    num_dummy_atoms = len(atoms) - num_original_atoms
    print(f"\nSuccessfully created augmented data file: '{filename}'")
    print(f"  Total Atoms: {len(atoms)} ({num_original_atoms} original + {num_dummy_atoms} dummy)")
    print(f"  Total Bonds: {len(bonds)}")


# --- Main execution ---
if __name__ == "__main__":
    print(f"Parsing '{original_data_file}'...")
    original_data = parse_lammps_data(original_data_file)

    print("Augmenting data structure...")
    new_atoms, new_bonds = augment_data(original_data,
                                        dummy_atoms_per_bond,
                                        arc_height)

    print(f"Writing new file '{augmented_data_file}'...")
    write_augmented_data(augmented_data_file,
                         new_atoms,
                         new_bonds,
                         original_data['headers'])