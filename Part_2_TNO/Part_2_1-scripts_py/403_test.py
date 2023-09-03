import compas_tno
from compas_tno.diagrams import FormDiagram
from compas_tno.shapes import Shape
from compas.datastructures import Mesh
from compas_tno.optimisers import Optimiser
from compas.rpc import Proxy
from compas_tno.rhino import FormArtist

intra_ad = '/Users/mricardo/compas_dev/me/segovia/intra.json'
extra_ad = '/Users/mricardo/compas_dev/me/segovia/extra.json'
form_ad = '/Users/mricardo/compas_dev/me/segovia/form.json'

intra = Mesh.from_json(intra_ad)
extra = Mesh.from_json(extra_ad)
form = FormDiagram.from_json(form_ad)

shape = Shape.from_meshes_and_formdiagram_proxy(form, intra, extra)
shape.datashape['thk'] = 0.25
shape.ro = 20.0

min_opt = Optimiser.create_minthrust_optimiser()

proxy = Proxy()
proxy.package = 'compas_tno.problems'
form, shape, optimiser = proxy.run_NLP_proxy2(form.to_data(), shape.to_data(), min_opt.to_data())

form = FormDiagram.from_data(form)
shape = Shape.from_data(shape)
optimiser = Optimiser.from_data(optimiser)

art = FormArtist(form)
art.draw_thrust()
art.draw_cracks()
art.draw_reactions()
art.redraw()
