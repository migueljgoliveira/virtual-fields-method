# Virtual Fields Method

[![Build Status](https://travis-ci.org/kubernetes-client/python.svg?branch=master)](https://travis-ci.org/kubernetes-client/python)
[![PyPI version](https://badge.fury.io/py/kubernetes.svg)](https://badge.fury.io/py/kubernetes)
[![codecov](https://codecov.io/gh/kubernetes-client/python/branch/master/graph/badge.svg)](https://codecov.io/gh/kubernetes-client/python "Non-generated packages only")
[![pypi supported versions]()]()

#### Dependencies

- Python, numpy (>= 1.21.5), scipy (>= 1.7.3), 


- `prjname` : name of project.

#### Data Files

The input data files should be located in a folder named `prjname` and inside the `input` folder located in the root directory. The required data files are as followes and should be named accordingly:
- `prjname`_Nodes.csv
    - Define nodes and its reference coordinates.
- `prjname`_Elements.csv
    - Defines elements connectivity.
- `prjname`\_U_`t`.CSV
    - Define nodes displacements (there should be one file for each time increment `t`)
- `prjname`_Orientation.csv
    - Define material orientation (in degrees) with respect to the loading direction.
- `prjname`_Thickness.csv
    - Define specimen thickness.
- `prjname`_Force.csv
    - Define load force evolution along each component.

#### Options File

An options file named `prjname`.vfm should be created and placed inside the input project folder. This file is used to define general options for the program. The keyword `**` is used as a comment. Keywords are case-insensitive. Several options are available as follows.

##### Required Keywords

- **`*Identification`** or **`*Simulation`** : Define type of computation.
  - Only one should be selected. 
  - **`*Identification`** is used to perform the parameter identification.
  - **`*Simulation`** is used to perform one run using the prescribed properties.

- **`*Tests`** Define the number and the name of tests.
  - Line 1: Give total number of tests.
  - Line 2: Give number and name of first test.
    - Repeat this data line as often as necessary to define the name of all tests.
    - The test name should correspond to the data files folder of each test.

- **`*Virtual Fields`** : Define type of virtual fields.
  - Line 1: Give the number of test and type of virtual field for given test, separated by a comma.
    - Options for type of virtual fields: `UD` (User-Defined) or `SB` (Sensivity-Based). 
  - Line 1: If `UD` option is selected, give numbers of the virtual fields to be used (e.g. `1`, `2`), after `UD` and separated by a comma. 
    - Repeat data line as often as necessary to define virtual fields for each test.
    - `SB` (Not yet available)

- **`*Properties`** : Define initial properties.
  - Line 1: Give total number of properties.
  - Line 2: Give property number and its initial value, separated by a comma.
    - The first property number should start at 0.
    - Repeat this data line as often as necessary to define all properties.
    - See UMMDp documentation for more information on the properties definition.

- **`*Variables`**: Define the identification parameters. 
  - Line 1: Give property number and identification flag (`0` or `1`), separated by a comma. 
    - Set identification flag to `0` to define a fixed property or to `1` to define an identification property.
    - Mandatory to repeat this data line as often as necessary to define all properties.

##### Optional Keywords

- **`*Output`** : Define output folder name.
  - Line 1: Give name of the output folder.
    - If this keyword is omitted the output folder defaults to `prjname`.
 
- **`*Nlgeom`** : Define small or large deformation framework.
  - Line 1: `0` (small deformation) or `1` (large deformation).framework. 
    - If this keyword is omitted defaults to large deformation framework.

- **`*Optimization`** : Define optimization parameters.
  - Line 1: Give the tolerance criterion and the maximum number of iterations, separated by a comma. 
    - If this keyword is omitted the tolerance is defaults to 1e-8 and the maximum number of iteratins to 500.

- **`*Boundaries`** : Define optimization boundaries for identification parameters.
  - Line 1: Give total number of identification parameters with optimization boundaries.
  - Line 2: Give property number, lower and upper boundaries, separeted by a comma. 
    - Repeat this data line as often as necessary to define all identification parameters with optimization boundaries.
    - To leave either the lower or upper boundary free, use `-inf` or `+inf`.

- **`*Constraints`** : Define constraints between properties.
  - Line 1: Give total number of properties with constraints.
  - Line 2: Give number of constrained property and constraint equation, separated by a comma.
    - The constraint equation should be defined using Python mathematical syntax (e.g. `[]`,`()`,`*`,`**`,`/`), and to call other properties can be used inside square brackets (e.g. to use property number 4 in the equation `[4]`).
    - Repeat this data line as often as necessary to define all properties with constraints.
