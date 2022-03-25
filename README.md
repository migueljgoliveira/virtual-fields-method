# Virtual Fields Method

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
  - **`*Identification`** is used to perform the parameters identification.
  - **`*Simulation`** is used to perform one run using the given properties.

- **`*Virtual Fields`** : Define type of virtual fields.
  - First Line: `UD` (User-Defined) or `SB` (Sensivity-Based).
  - `UD`
    - Line 1: Give types of user-defined virtual fields. Repeat this data line as often as necessary to define virtual fields for each test.
  - `SB` (Not Yet Available)

- **`*Properties`** : Define initial properties.
  - Line 1: Give number of properties.
  - Line 2: Give property number and its initial value. The first property should start at 0. Repeat this data line as often as necessary to define all properties.

- **`*Variables`**: Define properties to be identified. 
  - Line 1: Give property number and identification flag. Set identification flag to `0` to define a fixed property or to `1` to define an identification property. Repeat this data line as often as necessary to define all properties.

##### Optional Keywords

- **`*Tests`** Define tests.
  - Line 1: Give number of tests.
  - Line 2: Give name of first test. Repeat this data line as often as necessary to define the name of all tests. The test name should correspond to the data files folder of each test.
  - If this keyword is omitted only one test is considered named after `prjname`.

- **`*Output`** : Define output folder name.
  - Line 1: Give name of the output folder.
  - If this keyword is omitted the output folder is named after `prjname`.
 
- **`*Nlgeom`** : Define small or large deformation framework.
  - Line 1: `0` (small deformation) or `1` (large deformation).framework. 
  - If this keyword is omitted the large deformation framework is used.

- **`*Algorithm`** : Define optimization algorithm.
  - Line 1: `LM` (Levenberg-Marquardt) or `DE` (Differential Evolution).
  - If this keyword is omitted `LM` is used.


- **`*Boundaries`** : Define identification properties boundaries.
  - Line 1: Give number of identification properties with boundaries.
  - Line 2: Give property number, lower and upper boundaries. Repeat this data line as often as necessary to define all identification properties with boundaries.


- **`*Constraints`** : Define constraints between properties.
  - Line 1: Give number of properties with constraints.
  - Line 2: Give number of constrained property and constraint equation. The constraint equation should be defined using Python mathematical syntax, and other properties can be used inside square brackets. Repeat this data line as often as necessary to define all properties with constraints.
