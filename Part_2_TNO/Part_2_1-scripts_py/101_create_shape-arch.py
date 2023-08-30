from compas_tno.shapes import Shape

# Arch parameters
H = 1.0  # Height of arch
L = 2.0  # Span of arch (from center)
b = 0.5  # Out-of-plane distance
thk = 0.2  # Thickness of arch
discretisation = 20  # number of blocks

# Create arch
arch = Shape.create_arch(H=H, L=L, b=b, thk=thk, discretisation=discretisation)

# Measure arch selfweight
density = 20  # Density in kN/m3
arch.ro = density
swt = arch.compute_selfweight()
print('Arch SWT: {0:.2f} kN'.format(swt))