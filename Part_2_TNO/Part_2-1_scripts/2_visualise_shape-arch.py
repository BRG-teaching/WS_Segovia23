from compas_tno.shapes import Shape
from compas_tno.viewers import Viewer

# Arch parameters
H = 1.0  # Height of arch
L = 2.0  # Span of arch (from center)
b = 0.5  # Out-of-plane distance
thk = 0.2  # Thickness of arch
discretisation = 20  # number of blocks

# Create arch
arch = Shape.create_arch(H=H, L=L, b=b, thk=thk, discretisation=discretisation)

# Visualise
view = Viewer()
view.shape = arch
view.set_camera(target=[1, 1, 0], distance=7.0)
view.draw_shape()
view.show()
