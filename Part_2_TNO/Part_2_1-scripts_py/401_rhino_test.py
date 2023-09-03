# This script should be run at Rhino Python Editor

import compas_rhino
from compas_rhino.conversions import RhinoLine
from compas_rhino.conversions import RhinoPoint
from compas_rhino.conversions import RhinoMesh
from compas_tno.diagrams import FormDiagram
from compas_rhino.utilities import select_lines
from compas_rhino.utilities import select_points
from compas_rhino.utilities import select_meshes
from compas.geometry import distance_point_point
from compas.datastructures import Mesh
from compas_tno.shapes import Shape
from compas_tno.rhino import FormArtist
from compas_tno.optimisers import Optimiser
from compas.rpc import Proxy

guids = select_lines(message='Select the Lines for the Form Diagram Mesh')

lines = []
if not guids:
    print('Found no objects')
    pass
else:
    for guid in guids:
        rhinoline = RhinoLine.from_guid(guid)
        compasline = rhinoline.to_compas()
        lines.append(compasline)

compas_rhino.rs.UnselectObjects(guids)

compas_mesh = Mesh.from_lines(lines, delete_boundary_face=True)

form = FormDiagram.from_mesh(compas_mesh)

guids = select_points(message='Select the Supports in the Form Diagram')

if not guids:
    print('Found no objects')
    pass
else:
    supports = []
    for guid in guids:
        rhinopoint = RhinoPoint.from_guid(guid)
        compaspoint = rhinopoint.to_compas()
        supports.append(compaspoint)

    compas_rhino.rs.UnselectObjects(guids)

    sup = 0

    for key in form.vertices():
        pt = form.vertex_coordinates(key)
        for support in supports:
            if distance_point_point(support, pt) < 1e-3:
                form.vertex_attribute(key, 'is_fixed', True)
                sup +=1

print('Detected {} supports'.format(sup))

print(form)

guids = select_meshes(message='Select the intrados mesh')

if not guids:
    print('Found no objects')
    pass
else:
    for guid in guids:
        mesh = RhinoMesh.from_guid(guid)
        intra_mesh = mesh.to_compas()

compas_rhino.rs.UnselectObjects(guids)

guids = select_meshes(message='Select the extrados mesh')

if not guids:
    print('Found no objects')
    pass
else:
    for guid in guids:
        mesh = RhinoMesh.from_guid(guid)
        extra_mesh = mesh.to_compas()

compas_rhino.rs.UnselectObjects(guids)

print(intra_mesh)
print(extra_mesh)

intra_ad = '/Users/mricardo/compas_dev/me/segovia/intra.json'
extra_ad = '/Users/mricardo/compas_dev/me/segovia/extra.json'
form_ad = '/Users/mricardo/compas_dev/me/segovia/form.json'

intra_mesh.to_json(intra_ad)
extra_mesh.to_json(extra_ad)
form.to_json(form_ad)

shape = Shape.from_meshes_and_formdiagram_proxy(form, intra_mesh, extra_mesh)
shape.datashape['thk'] = 0.25
shape.ro = 20.0

print(shape)

# make options to find what is the objective
optimiser = Optimiser.create_minthrust_optimiser()

proxy = Proxy()
proxy.package = 'compas_tno.problems'
form, shape, optimiser = proxy.run_NLP_proxy2(form.to_data(), shape.to_data(), optimiser.to_data())

form = FormDiagram.from_data(form)
shape = Shape.from_data(shape)
optimiser = Optimiser.from_data(optimiser)

art = FormArtist(form)
art.draw_thrust()
art.draw_cracks()
art.draw_reactions()
art.redraw()