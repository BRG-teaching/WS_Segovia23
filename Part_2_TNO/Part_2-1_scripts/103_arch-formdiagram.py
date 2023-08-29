from compas_tno.shapes import Shape
from compas_tno.viewers import Viewer
from compas_tno.diagrams import FormDiagram

# Arch parameters
H = 1.0  # Height of arch
L = 2.0  # Span of arch (from center)
b = 0.5  # Out-of-plane distance
thk = 0.2  # Thickness of arch
discretisation = 20  # number of blocks

# Create arch
arch = Shape.create_arch(H=H, L=L, b=b, thk=thk, discretisation=discretisation)

# Create form diagram
form = FormDiagram.create_arch(H=H, L=L, discretisation=discretisation)

# Visualise
view = Viewer(form, arch)
view.set_camera(target=[1, 1, 0], distance=7.0)
view.draw_form()
view.draw_shape()
view.show()
