from compas_tno.shapes import Shape
from compas_tno.diagrams import FormDiagram
from compas_tno.viewers import Viewer
from compas_tno.analysis import Analysis

# Dome parameters
radius = 5.0  # Central radius of the dome
thk = 0.50  # Thickness of the dome
center = [5, 5, 0]  # coordinates of the center
dome = Shape.create_dome(radius=radius, thk=thk, center=center)

# Form diagram
discretisation = [16, 20]
form = FormDiagram.create_circular_radial_form(radius=radius, discretisation=discretisation)

# Create analysis for minimum thrust result
analysis = Analysis.create_minthrust_analysis(form,
                                              dome,
                                              printout=True,
                                              solver='SLSQP')

# Activate constraints, lump loads, set up and run analysis
analysis.optimiser.set_constraints(['funicular', 'envelope', 'reac_bounds'])
analysis.apply_selfweight()
analysis.apply_envelope()
analysis.apply_reaction_bounds()
analysis.set_up_optimiser()
analysis.run()

# Visualise 
view = Viewer(form, dome)
view.draw_form()
view.draw_shape()
view.draw_cracks()
view.show()