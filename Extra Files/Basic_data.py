#!/usr/bin/env python3
"""
generate_basic_theta_fixed_3_4.py
6 atoms, 10 bonds (double edges on sides)
3–4 bond now correctly connects (center aligned, not diverging)
"""

bridge = 4.0
arc_height = 1

# === FIXED ATOM COORDS ===
# Moved 3 and 4 closer to each other (smaller x, smaller vertical gap)
atoms = {
    1: (-bridge,  arc_height, 0.0),     # left-top
    2: (-bridge, -arc_height, 0.0),     # left-bottom
    3: (0.0,     1.5, 0.0),            # mid-top (closer to center)
    4: (0.0,    -1.5, 0.0),            # mid-bottom (closer to center)
    5: ( bridge,  arc_height, 0.0),     # right-top
    6: ( bridge, -arc_height, 0.0)      # right-bottom
}

# === BONDS ===
# Double bonds for 1–2 and 5–6
# 3–4 now connects correctly (shorter, centered)
bonds = [
    (1, 2),  # left double edge 1
    (1, 2),  # left double edge 2
    (3, 4),  # middle vertical (fixed)
    (5, 6),  # right double edge 1
    (5, 6),  # right double edge 2
    (1, 3),  # top-left bridge
    (3, 5),  # top-right bridge
    (2, 4),  # bottom-left bridge
    (4, 6),  # bottom-right bridge
]

# === WRITE LAMMPS DATA FILE ===
outname = "basic.data"
with open(outname, "w", newline="\n") as f:
    f.write("LAMMPS data file - Fixed 3–4 bond alignment (Theta structure)\n\n")
    f.write(f"{len(atoms)} atoms\n")
    f.write(f"{len(bonds)} bonds\n\n")
    f.write("1 atom types\n1 bond types\n\n")

    xs = [a[0] for a in atoms.values()]
    ys = [a[1] for a in atoms.values()]
    zs = [a[2] for a in atoms.values()]
    margin = 2.0
    f.write(f"{min(xs)-margin:.2f} {max(xs)+margin:.2f} xlo xhi\n")
    f.write(f"{min(ys)-margin:.2f} {max(ys)+margin:.2f} ylo yhi\n")
    f.write(f"{min(zs)-margin:.2f} {max(zs)+margin:.2f} zlo zhi\n\n")

    f.write("Masses\n\n1 12.011\n\n")

    f.write("Atoms # atomic\n\n")
    for i, (x, y, z) in atoms.items():
        f.write(f"{i} 1 {x:.3f} {y:.3f} {z:.3f}\n")

    f.write("\nBonds # bond\n\n")
    for i, (a1, a2) in enumerate(bonds, start=1):
        f.write(f"{i} 1 {a1} {a2}\n")

print(f"✅ Wrote {outname} with {len(atoms)} atoms and {len(bonds)} bonds (fixed 3–4 alignment)")
