from compas_tno.shapes import Shape
from compas_tno.diagrams import FormDiagram
from compas_tno.viewers import Viewer

# Dome parameters
radius = 5.0  # Central radius of the dome
thk = 0.50  # Thickness of the dome
center = [5, 5, 0]  # coordinates of the center
dome = Shape.create_dome(radius=radius, thk=thk, center=center)

# Form diagram
discretisation = [16, 20]
form = FormDiagram.create_circular_radial_form(radius=radius, discretisation=discretisation)

# Visualise 
view = Viewer(form, dome)
view.draw_form()
view.draw_shape()
view.show()