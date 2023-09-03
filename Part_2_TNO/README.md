# COMPAS Masonry workshop - Part 2 (TNO)

In part 2 of this workshop, you will learn how to use COMPAS TNO to assess existing masonry structures.

## 1. Introduction

COMPAS TNO is a Python package to find admissible thrust networks in masonry vaulted structures.

The package implements _Thrust Network Optimisation_, or TNO, within the COMPAS framework. TNO is a modular multi-objective optimisation framework to find admissible thrust networks in vaulted masonry structures. Thrust Networks represent the internal forces in masonry structures as a connected force network within the structural geometry. Based on the safe theorem of limit analysis, a structure is safe if at least one thrust network is found within its envelope. This set of compressive internal forces corresponds to a lower-bound equilibrium solution.

With TNO, multiple equilibrium states can be obtained, including the structure’s minimum and maximum horizontal thrusts, minimum thickness, vertical and horizontal collapse loads, and the internal stress following support movements. A nonlinear optimisation problem is formulated and solved in the background to find these specific structural solutions. TNO sets up, runs and outputs the solution networks to these problems.

In this workshop, we will go through the base functionalities of the plug-in to assess masonry structures. For the full documentation of COMPAS TNO, please visit the following pages:

* [COMPAS TNO Homepage](https://blockresearchgroup.github.io/compas_tno/)
* [COMPAS TNO API](https://blockresearchgroup.github.io/compas_tno/latest/api.html)

## 2. Preparation

If you have already installed the base configurations of the workshop, you are already all set to use the initial functionalities of COMPAS TNO. However, in this workshop, you will need to obtain a license to MOSEK to run convex optimisation problems. Instructions on how to get and install a MOSEK license are listed here:

* [Download and install MOSEK license](https://blockresearchgroup.github.io/compas_tno/latest/gettingstarted/solvers.html#mosek-1)

Optional: Another option to run convex problems is to use MATLAB. If you can not install a MOSEK license and are an experienced MATLAB user, you can install the CVX package in MATLAB following these instructions:

* [Optional: Set-up MATLAB and CVX](https://blockresearchgroup.github.io/compas_tno/latest/gettingstarted/solvers.html#mosek-1)

## 3. Basics

The workflow of **COMPAS TNO** is composed of the following elements summarised in the image below:

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/23ad55ca-136f-4ee9-a12b-ba9cb02cd29c">

The steps are numbered herein.

1. The [FormDiagram](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/1_form.html) defines the flow of forces in the structure.
2. The [Shape](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/2_shape.html) object defines the geometry of the masonry to be analysed.
3. The [Optimiser](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/3_optimiser.html) object stores the settings necessary to optimise.
4. The [Analysis](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/4_analysis.html) gathers the form diagram, shape and optimiser objects, performs preconditioning operations, runs the optimisation and visualises the solution.

You'll be able to go over the [TNO Tutorial](https://blockresearchgroup.github.io/compas_tno/latest/tutorial.html) to learn the role of these elements and how to create them. This workshop will focus on creating meaningful structural analysis using TNO. Different problems are studied in the following sections.

## 4. Arch analysis

This first example analyses a parametric arch and obtains the minimum and maximum horizontal thrusts.

**Arch geometry**

To create and visualise an arch, the Shape object is used. The following code can be written to create and visualise the shape of a hemispheric arch. Please note that only the intrados and extrados surfaces of the structure are displayed.

```python
from compas_tno.shapes import Shape
from compas_tno.viewers import Viewer

arch = Shape.create_arch()

view = Viewer()
view.shape = arch
view.draw_shape()
view.show()
```
<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/95567759-eeab-408a-a93b-bcaa7a19f9ac">

When the arch is created, additional parameters can be passed to control its geometric features properties, e.g., thickness, span, and length, as in the code below, where an arch with a thickness of 0.2m and a span of 2.0m is created. A 20 kN/m3 density is applied to the arch, and the self-weight is computed and printed.

```python
from compas_tno.shapes import Shape

# Arch parameters
H = 1.0  # Height of arch
L = 2.0  # Span of arch (from center)
b = 0.5  # Out-of-plane distance
thk = 0.2  # Thickness of arch
discretisation = 20  # number of divisions

# Create arch
arch = Shape.create_arch(H=H, L=L, b=b, thk=thk, discretisation=discretisation)

# Measure arch selfweight
density = 20  # Density in kN/m3
arch.ro = density
swt = arch.compute_selfweight()
print('Arch SWT: {0:.2f} kN'.format(swt))
```

```python
>> Arch SWT: 6.28 kN
```

**Form Diagram**

The second step for the analysis is defining a form diagram for the problem. For the arch problem, the form diagram is trivial and corresponds to a segmented line. The density of this line, i.e., the number of divisions on it, will correspond to the number of blocks in the structure. To create and visualise the form diagram with 20 blocks, the following code can be written:

```python
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

# Create form diagram
form = FormDiagram.create_arch(H=H, L=L, discretisation=discretisation)

# Visualise
view = Viewer(form, arch)
view.draw_form()
view.draw_shape()
view.show()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/df68def5-882e-4a77-bb1e-b7f2ee64522b">

**Minimum thrust analysis**

Now, we can create different analysis methods in the arch to find different admissible stress states in the arch. The first example searches for the minimum thrust result in the arch. An Analysis object is created and configured to seek minimum thrust results.

```python
from compas_tno.shapes import Shape
from compas_tno.viewers import Viewer
from compas_tno.analysis import Analysis
from compas_tno.diagrams import FormDiagram

# Arch parameters
H = 1.0  # Height of arch
L = 2.0  # Span of arch (from center)
b = 0.5  # Out-of-plane distance
thk = 0.2  # Thickness of arch

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
view.draw_form()
view.draw_shape()
view.draw_cracks()
view.show()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/375767a8-aa08-4804-a0e2-7b25f32ae57a">

In the solution, points where the thrust line touches the intrados (resp. extrados) are highlighted in blue (resp. green). These points indicate the locations where cracks form in the structures.

**Maximum thrust analysis**

Alternatively, the maximum thrust is obtained by modifying the analysis as below and running the entire snipped above with the updated objective.

```python
# Create analysis for maximum thrust result
analysis = Analysis.create_maxthrust_analysis(form,
                                              arch,
                                              printout=True,
                                              solver='SLSQP')
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/d168a086-325a-44b7-8d0c-b112d561bba3">

A series of other objectives can also be incorporated into this problem. For this, see the [types of analyses](https://blockresearchgroup.github.io/compas_tno/latest/api/generated/compas_tno.analysis.Analysis.html#compas_tno.analysis.Analysis) that can be created.

## 5. Dome analysis

**Dome Geometry**

Similarly, other three-dimensional shapes can also be created with TNO, as shown below for a dome having a radius of 5.0m and a thickness of 0.5m:

```python
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
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/7054eb66-54e6-431d-bd4b-92af43b23374">

**Dome Form Diagram**

The form diagram of the dome needs to be created. Unlike the arch, more parameters should be taken into account. A diagram based on 16 hoops and 20 meridians is defined with the following code that will be used in the analysis.

```python
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
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/a31fa55d-2868-43eb-9620-5c97935f24b3">

**Minimum thrust result**

Since the geometry and the form diagram are defined, the analysis can proceed with different objective functions, e.g., for obtaining the minimum thrust, the following code applies:

```python
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
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/55369354-bd59-4a30-9ea6-09f61ae3d054">

**Dome subjected to split displacement**

Another internal state of interest is the internal stress state for the masonry on the verge of the foundation displacement, which can be obtained with the minimisation of the complementary energy. In the following code, a splitting displacement field is applied to the supports of the dome, splitting the structure over the y-axis. The code below shows how to analyse this problem:

```python
from compas_tno.shapes import Shape
from compas_tno.diagrams import FormDiagram
from compas_tno.viewers import Viewer
from compas_tno.analysis import Analysis
from compas.geometry import Vector, Point
from numpy import array


# 1. Shape geometric definition
radius = 5.0
thk = 0.50
center = [5, 5]
dome = Shape.create_dome(radius=radius, thk=thk, center=center)
dome.ro = 1.0

# 2. Form diagram geometric definition
discretisation = [16, 20]
form = FormDiagram.create_circular_radial_form(radius=radius, discretisation=discretisation)

# 3. Define displacement field
vector_supports = []
vectors_plot = []
base_plot = []
xc = center[0]

for key in form.vertices_where({'is_fixed': True}):
    x, y, z = form.vertex_coordinates(key)
    dXbi = [0, 0, 0]
    if x - xc > 0.1:
        dXbi = [1, 0, 0]
        vectors_plot.append(Vector(*dXbi))
        base_plot.append(Point(x, y, z))
    if x - xc < -0.1:
        dXbi = [-1, 0, 0]
        vectors_plot.append(Vector(*dXbi))
        base_plot.append(Point(x, y, z))

    vector_supports.append(dXbi)

dXb = array(vector_supports)

# 4. Create analysis, run and visualise
analysis = Analysis.create_compl_energy_analysis(form, dome, solver='IPOPT', support_displacement=dXb, printout=True)
analysis.optimiser.set_constraints(['funicular', 'envelope', 'reac_bounds'])
analysis.apply_selfweight()
analysis.apply_envelope()
analysis.apply_reaction_bounds()
analysis.set_up_optimiser()
analysis.run()

view = Viewer(form, dome)
view.scale_edge_thickness(5.0)
view.draw_form()
view.draw_shape()
view.draw_reactions(extend_reactions=True)
view.draw_cracks()
for i in range(len(vectors_plot)):
    vector = vectors_plot[i]
    base = base_plot[i]
    view.draw_vector(vector=vector, base=base)
view.show()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/5f37e401-7fca-47c6-9cad-9842bd5c41c2">

## 6. Cross vault analysis

**Geometry and form diagram**

Within COMPAS TNO library, cross and pavillion vaults are also included and can be described parametrically. The following code generates and visualise a cross vault with the following parameters: span of 10.0m covering the x and y coordinates from 0 to 10.0; thickness t=0.50m and springing angle b=30deg.  

```python
from compas_tno.shapes import Shape
from compas_tno.diagrams import FormDiagram
from compas_tno.viewers import Viewer

# 1. Shape geometric definition
spr_angle = 30.0
L = 10.0
thk = 0.50
xy_span = [[0, L], [0, L]]
vault = Shape.create_crossvault(xy_span=xy_span, thk=thk, spr_angle=30)

# 2. Form diagram geometric definition
discretisation = 10
form = FormDiagram.create_cross_form(xy_span=xy_span, discretisation=discretisation)

view = Viewer(form)
view.draw_form()
view.draw_shape()
view.show()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/edb188f6-858c-4d0f-a473-9dd58935acf8">

**Minimum and maximum thrusts**

Given the form diagram and shape obtained in the previous section, minimum and maximum thrust states can be obtained by adding to the scripts proper analysis objects for each objective. The following snippets will compute and visualise the minimum and maximum horizontal thrust solutions for the cross vault problem.

```python
# 3. Minimum thrust solution and visualisation
analysis = Analysis.create_minthrust_analysis(form, vault, printout=True)
analysis.apply_selfweight()
analysis.apply_envelope()
analysis.set_up_optimiser()
analysis.run()

view = Viewer(form)
view.show_solution()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/d3ef07e0-02a6-4fac-b84e-de540194def4">

```python
# 4. Maximum thrust solution and visualisation
analysis = Analysis.create_maxthrust_analysis(form, vault, printout=True)
analysis.apply_selfweight()
analysis.apply_envelope()
analysis.set_up_optimiser()
analysis.run()

view = Viewer(form)
view.show_solution()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/406ceadb-fa09-44e1-9a15-14eb14579ea3">

**Maximum applied load at ridge**

Another possible objective is the maximisation of a given concentrated load applied to a vertex in the network. In the following script, the load is added to the node with planat coordinates y=3.125 x=5.0. To ensure the transfer of the applied load to the supports, additional straight members are added to the diagram. The following script computed the thrust network resultant from this applied vertical load.

```python
from compas_tno.shapes import Shape
from compas_tno.diagrams import FormDiagram
from compas_tno.viewers import Viewer
from compas_tno.analysis import Analysis
from compas_tno.plotters import TNOPlotter
from compas.geometry import distance_point_point_xy
from compas_tno.utilities import form_add_lines_support
from numpy import zeros
from compas_view2.objects import Arrow
from compas.colors import Color


# 1. Shape geometric definition
spr_angle = 30.0
L = 10.0
thk = 0.50
xy_span = [[0, L], [0, L]]
vault = Shape.create_crossvault(xy_span=xy_span, thk=thk, spr_angle=30)

# 2. Form diagram with additional line to supports
discretisation = 16
form = FormDiagram.create_cross_form(xy_span=xy_span, discretisation=discretisation)

load_pos = 3
xc = yc = L/2
yp = 2.5
yp = yc - load_pos/(discretisation/2) * yc
for key in form.vertices():
    pt = form.vertex_coordinates(key)
    if distance_point_point_xy(pt, [xc, yp, 0.0]) < 1e-3:
        loaded_node = key
        break

supports = []
for key in form.vertices_where({'is_fixed': True}):
    x, y, z = form.vertex_coordinates(key)
    if y < yc:
        supports.append(key)

print(loaded_node, supports)

form, loaded_node = form_add_lines_support(form, loaded_node=loaded_node, supports=supports)

plotter = TNOPlotter(form)
plotter.draw_form(scale_width=False, color=Color.black())
plotter.draw_supports(color=Color.red())
plotter.show()

# 3. Define applied load case
n = form.number_of_vertices()
load_direction = zeros((n, 1))
load_direction[loaded_node] = -1.0
print('New Loaded Node:', loaded_node)

# 4. Maximum load problem and visualisation
analysis = Analysis.create_max_load_analysis(form, vault, 
                                             load_direction=load_direction, 
                                             max_lambd=300, 
                                             printout=True,
                                             solver='SLSQP')
analysis.apply_selfweight()
analysis.apply_envelope()
analysis.set_up_optimiser()
analysis.run()

viewer = Viewer(form)
viewer.settings['scale.reactions'] = 0.004
viewer.draw_thrust()
viewer.draw_cracks()
viewer.draw_shape()
viewer.draw_reactions()

length = 2.0
x, y, z = form.vertex_coordinates(loaded_node)
z += length + 0.1
arrow = Arrow([x, y, z], [0, 0, -length])
viewer.app.add(arrow, linecolor=(0, 0, 0), facecolor=(0, 0, 0))

viewer.show()
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/be0ad7e2-73c4-474a-b668-42d4f6c7004a">

## 7. Interactive example in Rhinoceros

The final example of the workshop presents a structure that was analysed in the 2021 edition of the HIMASS workshop. It's the assessment of St. Angelo church in Anagni, Italy. A Rhino file is placed in the repository titled ``vault_example-TNO.3dm``. When you open the file, it should look like in the following figure:

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/aba99aec-bf0d-4156-a1ca-1ce0ab0c2624">

Important: To execute script ``401_rhino_example.py`` in the repository, you will need to have installed TNO for Rhino as explained here:

- [Install TNO in Rhino](https://blockresearchgroup.github.io/compas_tno/latest/gettingstarted/rhino.html)

In the layers of the Rhino file you will find the following:

- form_1: the lines of the form diagram that we are going to use,
- form_2: empty layer for you to draw your form diagram,
- extrados: with the extrados mesh of the vault in St. Angelo,
- intrados: with the intrados mesh of the vault in St. Angelo,
- supports: the supports of the form diagram,
- displacements: vectors that we will use to apply displacement in the vault,
- loads: load vectors that we will apply in the vault.

To run a script in Rhino you need to type the command ``RunPythonScript`` and then navigate and open script ``401_rhino_example.py`` where you saved it.

The script will ask for successive inputs to run the analysis for you. For example. For the Minimum and maximum thrust analysis

1. **Select the lines for the form diagram:** select the lines in layer form_1
2. **Select the supports in the form diagram:** select the supports in support layer corresponding to the 4 corners of the structure
3. **Select the intrados mesh:** select the intrados mesh
3. **Select the extrados mesh:** select the extrados mesh
4. **Set density of masonry:** the value of 20 kN/m3 is suggested
5. **Set the average thickness of masonry:** write the average thickness of the vault (default 0.25m)
6. **Set Objective of the Analysis:** four options appear: minimum thrust / maximum thrust / displacement / Maximum load. Select the analysis desired for your purpose and continue.

If you select the minimum or maximum thrust objectives, the analysis will run and display the solution. 

For the minimum thrust solution the following is obtained:

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/8c1677c2-f6dd-4c91-9434-06873c4a36ce">

Note that new layers were created with the solution and sublayers to display individual axial forces, etc.

If you proceed with the analysis for displacement or loads, you will be asked to provide the vector for displacing the supports or the external loads. For displacements: 

8. **(Optional)Select displacement at foundations:** Here, you will be asked to provide one (or multiple) vectors corresponding to the supports of the vault. If you'd like to continue adding vectors, please feel free to press to continue it. Only vectors related to supports defined in the form diagram can be input. Since we only supported the four corners, only corner displacements are acceptable. In the layer ``displacements`` a pair of example supports is given. Note that the starting point needs to match the projection of the support in the form diagram.

The solution expected for the pair of support displacements is shown below. It corresponds to the network after the right side of the vault suffered an infinitesimal settlement.

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/15d6d1a5-fba6-419f-90aa-8639b355f449">

If the goal is to maximize vertical applied loads the instruction is:

8. **(Optional)Select external loads:** Loads must be vertical and also applied at points that project into nodes on the form diagram. Layer ``loads`` come with three-point loads that can be added as an example. The objective function will maximize the multiplier of that load. When the solution appears ``fopt`` will represent the maximum multiplier obtained by the solver.

The expected solution is presented below. The optimal value of the problem (129.84) enables to compute the total load applied. The vectors were unitary so, the total load applied is 3*129.8 kN = 389.4 kN.

<img width="1049" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/1af60372-542c-4401-9b2b-5f522b80e1ef">

## Do it yourself

By adapting the parametric models presented at this workshop and playing with the script provided for analysing vaults from Rhino, users can analyse a wide range of 3D problems in masonry structures. Go ahead and use TNO in your next project. 

If you have further questions, please address them to mricardo@ethz.ch.
