# OVITO Python Script for Better Visualization
# Run this in OVITO's Python script modifier or as standalone script

from ovito.io import import_file
from ovito.modifiers import *
from ovito.vis import *

# Load trajectory
pipeline = import_file('theta_polymer.lammpstrj')

# Create bonds based on proximity
bond_mod = CreateBondsModifier(cutoff=2.0, mode=CreateBondsModifier.Mode.Pairwise)
pipeline.modifiers.append(bond_mod)

# Adjust particle display
pipeline.modifiers.append(AssignColorModifier(
    color=(0.2, 0.8, 0.3)  # Green color
))

# Increase particle size for main atoms
def modify_particles(frame, data):
    positions = data.particles_.positions
    radii = data.particles_.create_property('Radius')

    # Make first 6 atoms (main vertices) larger
    for i in range(min(6, len(positions))):
        radii[i] = 0.5

    # Intermediate atoms smaller
    for i in range(6, len(positions)):
        radii[i] = 0.2

pipeline.modifiers.append(PythonScriptModifier(function=modify_particles))

# Configure rendering
particles = pipeline.source.data.particles.vis
particles.radius = 0.3

bonds = pipeline.source.data.bonds.vis
bonds.width = 0.15
bonds.shading = ParticleVis.Shading.Flat
bonds.color = (0.1, 0.6, 0.2)  # Dark green bonds

print("Visualization setup complete!")
print("Adjust camera angle to see the loop structure clearly")
