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

**Dome Geometry**

International Summer School on Historic Masonry - Segovia 2023

*Computational assessment of masonry structures*

* https://www.himass.org/
* https://github.com/compas-dev/compas
* https://github.com/BlockResearchGroup/compas_assembly
* https://github.com/BlockResearchGroup/compas_cra
* https://github.com/BlockResearchGroup/compas_tno

![Segovia 2023](images/himass.png)

## Schedule

**Wednesday 30/08/2023**

Time | Topic
---  | ---
18.15 - 19.30 | Lecture Prof. Philippe Block

**Friday 01/09/2023**

Time | Topic
---  | ---
18.15 - 18.50 | Lecture on Discrete Element Modelling (DEM) - Dr. Alessandro Dell'Endice
18.55 - 19.30 | Lecture on Thrust Network Analysis (TNA) - Dr. Ricardo Maia Avelino
 
**Monday  04/09/2023**

Time | Topic
---  | ---
15.00 - 16.30 | COMPAS Masonry workshop - Part 1 (CRA) - Dr. Alessandro Dell'Endice
17.00 - 18.15 | COMPAS Masonry workshop - Part 2 (TNO) - Dr. Ricardo Maia Avelino

</br>

## Preparations

**1. Requirements**

* [Anaconda 3](https://www.anaconda.com/distribution/)
* [Rhino 6/7](https://www.rhino3d.com/download)
* [Visual Studio Code](https://code.visualstudio.com/): Any python editor works, but we recommend [VSCode + extensions](https://compas.dev/compas/latest/gettingstarted/vscode.html)

During the installation of the various tools, just accept all default settings.
The default location for installing Anaconda is usually in the home directory.
If it isn't, try to install it there anyway.
And make sure not to register it on the `PATH` (Windows only).
On Windows, the path to the home directory is stored in the variable `%USERPROFILE%`.
On Mac, it is accessible through `~`.
This results in the following recommended installation directories for Anaconda.

*On Windows*

```
%USERPROFILE%\Anaconda3
```

*On Mac*

```
~/anaconda3
```

## Installation

** The command line**

Many instructions in the next sections will have to be run from "the command line".

On Windows, use the "Anaconda Prompt" instead of the "Command Prompt", and make sure to run it *as administrator*.

> To find the Anaconda Prompt open the Start Menu and type "Anaconda".
> The Anaconda Prompt should already show up in the list of search results.
> To launch is as administrator, right click and select "Run as administrator".

On Mac, use the "Terminal".

**For simplicity, this guide will refer to both Terminal and Anaconda Prompt as "the command line".**

![The command line](images/command_line.png)

We will use the command line to install the COMPAS Python packages (and their dependencies) required for the workshop.

> **NOTE**: If you're on Windows, all commands below have to be executed in the *Anaconda Prompt* (NOT the *Command Prompt*)

We use `conda` to make sure we have clean, isolated environment for dependencies.

<details><summary>First time using <code>conda</code>?</summary>
<p>

Make sure you run this at least once:

    (base) conda config --add channels conda-forge

</p>
</details>

    (base) conda env create -f https://github.com/BRG-teaching/WS_Segovia23/blob/main/environment.yml

### Add to Rhino

    (base)  conda activate WS_Segovia23
    (WS_Segovia23) python -m compas_rhino.install -v 7.0

If this is the first time you are using Rhino for Windows, or if you have never opened its
PythonScriptEditor before, do so now: open Rhino and open the editor by typing `EditPythonScript`.
Then simply close Rhino again.

To check the installation, launch Rhino, open the PythonScriptEditor, and try
importing the COMPAS packages in a script.
Then run the script and if no errors pop up, you are good to go.

```python
import compas
import compas_rhino
import compas_assembly
```

![Test Rhino](images/test-rhino.png)

### Get the workshop files

Clone the repository:

```
(WS_Segovia23) cd Documents
(WS_Segovia23) git clone https://github.com/BRG-teaching/WS_Segovia23.git
```

### Verify installation

    (WS_Segovia23) python -m compas

    Yay! COMPAS is installed correctly!

    COMPAS: 1.17.0
    Python: 3.9.13 (CPython)
    Extensions: ['compas-cgal', 'compas-gmsh', 'compas-rrc', 'compas-fab', 'compas-occ', 'compas-view2']

## Help

If you need help with the installation process, please post a note on the workshop Slack channel: 

Otherwise, you can also contact us via email at dellendice@arch.ethz.ch.


