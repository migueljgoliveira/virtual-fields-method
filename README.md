# Virtual Fields Method

## Data Files

* `prjname`_Nodes.csv

    |Node |X     |Y     |Z     |
    |:---:|:----:|:----:|:----:|
    | 0   |`X_0` |`Y_0` |`Z_0` |
    | 1   |`X_1` |`Y_1` |`Z_1` |
    |`...`|`...` |`...` |`...` |
    |`n`  |`X_n` |`Y_n` |`Z_n` |

* `prjname`_Elements.csv

    | Element | Node-1 | Node-2 | Node-3 | Node-4 |Node-5 | Node-6 | Node-7 | Node-8 |
    |:-------:|:------:|:------:|:------:|:------:|:-----:|:------:|:------:|:------:|
    | 0       |`EL0_0`   |`Y0`  |`Z0`  |1     |1     |1|1|
    | ...     | ...    | ...    | ...    | ...    | ...   | ...    | ...    | ...    |
    |`ne` |`Xnn`|`Ynn`|`Znn`|1|||||

* `prjname`_Uss_.CSV
* `prjname`_Orientation.csv

    |  Orientation  |
    |:-------------:|
    | `orientation` |

* `prjname`_Thickness.csv
  
    |  Thickness  |
    |:-----------:|
    | `thickness` |

* `prjname`_Force.csv

    | Time | Force-X | Force-Y | Force-Z |
    |:----:|:-------:|:-------:|:-------:|
    | 0    | `Fx_0`  | `Fy_0`  | `Fz_0`  |
    | 1    | `Fx_1`  | `Fy_1`  | `Fz_1`  |
    | ...  | ...     | ...     | ...     |
    | `t`  | `Fx_t`  | `Fy_t`  | `Fz_t`  |
