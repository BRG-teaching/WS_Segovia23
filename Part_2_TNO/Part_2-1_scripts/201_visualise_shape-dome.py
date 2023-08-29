from compas_tno.shapes import Shape
from compas_tno.viewers import Viewer

# Dome parameters
radius = 5.0  # Central radius of the dome
thk = 0.50  # Thickness of the dome
center = [5, 5, 0]  # coordinates of the center
dome = Shape.create_dome(radius=radius, thk=thk, center=center)

# Visualise
view = Viewer()
view.shape = dome
view.draw_shape()
view.show()
