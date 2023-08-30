from compas_tno.shapes import Shape
from compas_tno.viewers import Viewer
from compas_tno.analysis import Analysis
from compas_tno.diagrams import FormDiagram

# Arch parameters
H = 1.0  # Height of arch
L = 2.0  # Span of arch (from center)
b = 0.5  # Out-of-plane distance
thk = 0.2  # Thickness of arch
discretisation = 20  # number of blocks

# Create arch
arch = Shape.create_arch(H=H, L=L, b=b, thk=thk, discretisation=discretisation)
arch.ro = 200

# Create form diagram
form = FormDiagram.create_arch(H=H, L=L, discretisation=discretisation)

# Create analysis for minimum thrust result
analysis = Analysis.create_minthrust_analysis(form,
                                              arch,
                                              printout=True,
                                              solver='SLSQP')

# activate constraints, lump loads, set up and run analysis
analysis.optimiser.set_constraints(['funicular', 'envelope', 'reac_bounds'])
analysis.apply_selfweight()
analysis.apply_envelope()
analysis.apply_reaction_bounds()
analysis.set_up_optimiser()
analysis.run()

# Visualise
view = Viewer(form, arch)
view.set_camera(target=[1, 1, 0], distance=7.0)
view.draw_form()
view.draw_shape()
view.draw_cracks()
view.show()
