# This script should be run in Rhino

import compas_rhino
from compas_rhino.conversions import RhinoLine
from compas_rhino.conversions import RhinoPoint
from compas_rhino.conversions import RhinoMesh
from compas_tno.diagrams import FormDiagram
from compas_rhino.utilities import select_lines
from compas_rhino.utilities import select_points
from compas_rhino.utilities import select_meshes
from compas.geometry import distance_point_point_xy
from compas.datastructures import Mesh
from compas_tno.shapes import Shape
from compas_tno.rhino import FormArtist
from compas_tno.optimisers import Optimiser
from compas.rpc import Proxy


def select_vectors():
    vecs = []
    while True:
        vec = compas_rhino.rs.GetLine(mode=0, message1='Select Start Point of the Vector', 
                                      message2='Select End Point of the Vector')
        if vec:
            line = RhinoLine.from_geometry(vec).to_compas()
            vecs.append(line)
        cont = compas_rhino.rs.GetString("Set more vectors?", "False", ["True", "False", "Cancel"])
        if cont in ["True"]:
            pass
        else: 
            break
    
    return vecs

# ---------------------------
# 1. Create Form Diagram
# ---------------------------

compas_rhino.utilities.clear_layers(['FormDiagram'])  # clear previous solutions

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
            if distance_point_point_xy(support, pt) < 1e-3:
                form.vertex_attribute(key, 'is_fixed', True)
                sup +=1

print('Detected {} supports'.format(sup))

# ---------------------------
# 2. Create Shape
# ---------------------------

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

rho = compas_rhino.rs.GetString("Set density of masonry (kN/m3)", "20.0")
if not rho:
    raise ValueError('Please give a density to masonry (eg. 20.0)')
else:
    rho = float(rho)
    
thk = compas_rhino.rs.GetString("Set an average thickness (m)", "0.25")
if not thk:
    raise ValueError('Please give an average thickness (eg. 0.20)')
else:
    thk = float(thk)

# ---------------------------
# 3. Define Objective
# ---------------------------

option = compas_rhino.rs.GetString("Set Objective of the Analysis", "Cancel",
                                   ["min_thrust", 
                                    "max_thrust", 
                                    "displacement", 
                                    "max_load"])
if not option or option == "Cancel":
    print('Error!')

if option == 'min_thrust':
    optimiser = Optimiser.create_minthrust_optimiser()
elif option == 'max_thrust':
    optimiser = Optimiser.create_maxthrust_optimiser()
elif option == 'displacement':
    Xb = sup * [[0, 0, 0]]  # create empty displacement matrix
    vecs = select_vectors()
    for vec in vecs:
        displ = [vec[1][0]-vec[0][0], vec[1][1]-vec[0][1], vec[1][2]-vec[0][2]]
        xy = [vec[0][0], vec[0][1], 0.0]
        for i, key in enumerate(form.fixed()):
            pt = form.vertex_coordinates(key)
            if distance_point_point_xy(xy, pt) < 1e-2:
                Xb[i] = displ
                print('Support displacement', displ, 'applied to node', key)
    optimiser = Optimiser.create_compl_energy_optimiser(support_displacement=Xb)
elif option == "max_load":
    Pvz = form.number_of_vertices() * [[0]]
    vecs = select_vectors()
    for vec in vecs:
        load = - abs(vec[1][2]-vec[0][2])  # only z component
        xy = [vec[0][0], vec[0][1], 0.0]
        for i, key in enumerate(form.vertices()):
            pt = form.vertex_coordinates(key)
            if distance_point_point_xy(xy, pt) < 1e-2:
                Pvz[i] = [load]
                print('Load:', load, 'kN applied to node', key)
    optimiser = Optimiser.create_max_vertload_optimiser(max_lambd=500.0, load_direction=Pvz, solver='SLSQP')
else:
   raise ValueError('It seems like you selected an invalid option for the objective')

shape = Shape.from_meshes_and_formdiagram_proxy(form, intra_mesh, extra_mesh)
shape.datashape['thk'] = thk
shape.ro = rho

# ---------------------------
# 4. Run analysis (Proxy)
# ---------------------------

proxy = Proxy()
proxy.package = 'compas_tno.problems'
form, shape, optimiser = proxy.run_NLP_proxy2(form.to_data(), 
                                              shape.to_data(), 
                                              optimiser.to_data())

form = FormDiagram.from_data(form)
shape = Shape.from_data(shape)
optimiser = Optimiser.from_data(optimiser)

# ---------------------------
# 5. Display
# ---------------------------

art = FormArtist(form)
art.draw_thrust()
art.draw_forcepipes()
art.draw_cracks()
art.draw_reactions()
art.draw_forcelabels()
art.redraw()

if compas_rhino.rs.LayerVisible("FormDiagram::ForceLabels"):
    compas_rhino.rs.LayerVisible("FormDiagram::ForceLabels", False)

message = optimiser.message + ' fopt: ' + str(round(optimiser.fopt, 2))
compas_rhino.display_message(message)