from compas.datastructures import Mesh
from compas_tno.diagrams import FormDiagram
from compas_tno.shapes import Shape
from compas_tno.analysis import Analysis
from compas_tno.viewers import Viewer

intra_ad = '/Users/mricardo/compas_dev/me/segovia/intra.json'
extra_ad = '/Users/mricardo/compas_dev/me/segovia/extra.json'
form_ad = '/Users/mricardo/compas_dev/me/segovia/form.json'

intra = Mesh.from_json(intra_ad)
extra = Mesh.from_json(extra_ad)
form = FormDiagram.from_json(form_ad)

shape = Shape.from_meshes_and_formdiagram(form, intra, extra)
shape.datashape['thk'] = 0.25
shape.ro = 20.0

analysis = Analysis.create_minthrust_analysis(form, shape)
analysis.apply_selfweight()
analysis.apply_envelope()

analysis.set_up_optimiser()
analysis.run()

v = Viewer(form, shape)
v.draw_thrust()
v.draw_shape()
v.draw_reactions()
v.show()