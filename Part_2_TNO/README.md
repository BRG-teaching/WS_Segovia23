# COMPAS Masonry workshop - Part 2 (TNO)

In part 2 of this workshop, you will learn how to use COMPAS TNO to assess existing masonry structures.

## Introduction

COMPAS TNO is a Python package to find admissible thrust networks in masonry vaulted structures.

The package implements _Thrust Network Optimisation_, or TNO, within the COMPAS framework. TNO is a modular multi-objective optimisation framework to find admissible thrust networks in vaulted masonry structures. Thrust Networks represent the internal forces in masonry structures as a connected force network contained within the structural geometry. Based on the safe theorem of limit analysis, a structure is safe if at least one thrust network is found within its envelope. This set of compressive, internal forces corresponds to a lower-bound equilibrium solution.

With TNO, multiple particular equilibrium states can be obtained, including the structure’s minimum and maximum horizontal thrusts, its minimum thickness, its vertical and horizontal collapse loads, and the internal stress following support movements. To find these specific structural solutions, a nonlinear optimisation problem is formulated and solved in the background. TNO sets up, runs and outputs the solution networks to these problems.

In this workshop, we will go through the base functionalities of the plug-in to assess masonry structures. For the full documentation of COMPAS TNO, please visit the following pages:

* [COMPAS TNO Homepage](https://blockresearchgroup.github.io/compas_tno/)
* [COMPAS TNO API](https://blockresearchgroup.github.io/compas_tno/latest/api.html)

## Preparation

If you already installed the base configurations of the workshop you are already all set to use the initial functionalities of COMPAS TNO. However, in this workshop you will need to obtain a license to MOSEK to run convex optimisation problems. Instructions on how to get and install a MOSEK license are listed here:

* [Download and install MOSEK license](https://blockresearchgroup.github.io/compas_tno/latest/gettingstarted/solvers.html#mosek-1)

Optional: Another option to run convex problems is to use MATLAB. If you can not install a MOSEK license and are an experieced MATLAB user, you can install the SDPT3 solver in MATLAB following these instructions:

* [Optional: Set-up MATLAB and CVX](https://blockresearchgroup.github.io/compas_tno/latest/gettingstarted/solvers.html#mosek-1)

## Basics

The workflow of **COMPAS TNO** is composed by the following four main elements summarised in the image below:

<img width="800" alt="image" src="https://blockresearchgroup.github.io/compas_tno/latest/_images/workflow.png">

The steps are numbered herein.

1. The [FormDiagram](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/1_form.html) defines the flow of forces in the structure.
2. The [Shape](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/2_shape.html) object defines the geometry of the masonry to be analysed.
3. The [Optimiser](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/3_optimiser.html) object stores the settings that will be necessary to perform the optimisation.
4. The [Analysis](https://blockresearchgroup.github.io/compas_tno/latest/tutorial/4_analysis.html) gathers the form diagram, shape and optimiser objects, performs preconditioning operations, runs the optimisation and visualises the solution.

Below, we'll learn how to create these elements in the following parts of the tutorial.

## Arch analysis

This first example analyses a parametric arch and obtain the minimum and maximum horizontal thrusts.

**Arch geometry**

To create and visualise an arch, the Shape object is used. The following code can be written:

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

When the arch is created, additional parameters can be passed to control its geometric features properties, e.g., thickness, span, length as in the code below, where an arch with thickness of 0.2m and span of 2.0m is created. A density of 20 kN/m3 is applied to the arch and the selfweight is computed and printed.

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

**Form Diagram**

The second step for the analysis is the definition of a form diagram to the problem. At the arch problem, the form diagram is trivial and corresponds to a segmented line. To create and visualise the form diagram, the following code can be written:

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

![image](https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/df68def5-882e-4a77-bb1e-b7f2ee64522b)

**Minimum thrust analysis**

Now, we can create different analysis methods in the arch to find different admissible stress states in the arch. The first example searches for the minimum thrust result in the arch. An Analysis object is created and configured to seek for minimum thrust results.

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

**Maximum thrust analysis**

Alternativelly, by modifying the analysis type to a maximum thrust analysis, the maximum thrust is obtained.

```python
# Create analysis for maximum thrust result
analysis = Analysis.create_maxthrust_analysis(form,
                                              arch,
                                              printout=True,
                                              solver='SLSQP')
```

<img width="800" alt="image" src="https://github.com/BRG-teaching/WS_Segovia23/assets/36137188/d168a086-325a-44b7-8d0c-b112d561bba3">

A series of other objectives can also be incorporated in this problem. For this see the [types of analyses](https://blockresearchgroup.github.io/compas_tno/latest/api/generated/compas_tno.analysis.Analysis.html#compas_tno.analysis.Analysis) that can be created.

## Dome analysis

**Dome Geometry**

Similarly, other three dimensional shapes can also be created with TNO as shown below for a dome having radius of 5.0m and thickness of 0.5m:

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

The form diagram of the dome needs to be created. Unlike the arch, there are more parameters that should be taken into account. A diagram based on a certain number of hoops and meridians is defined with the following code that will be used in the analysis.

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

Since the geometry and the form diagram are defined, the analysis can proceed with different objective functions, e.g., for obtaining the minimum thrust the following code applies:

```phyhon
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

Another internal state of interests is the internal stress state for the masonry in the verge of the foundations displacement, which can be obtained with the minimisation of the complementary energy using the following code, where first the 

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

## Cross vault analysis

...
