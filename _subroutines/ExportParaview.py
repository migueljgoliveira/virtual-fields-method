import os
import shutil
import meshio
import numpy as np

import _subroutines

def ExportParaview(coord,conn,displ,strain,stress,vfs,dof,nf,nvfs,out):
    """
    Export experimental finite element mesh to paraview file.

    Parameters
    ----------
    eFEM : dict
        Final experimental finite element mesh dict.
    dir : str
        Directory of project to export output files.
    """

    # Swap out-of-plane shear components for paraview notation
    if dof == 3:
        strain = strain[...,[0,1,2,3,5,4]]
        stress = stress[...,[0,1,2,3,5,4]]

    # Nodes and elements connectivity
    points = coord
    if dof == 2:
        cells = [('quad',conn)]
    elif dof == 3:
        cells = [('hexahedron',conn)]

    # Output paraview file
    outF = f'{os.getcwd()}\\output\\{out}\\{out}'
    with meshio.xdmf.TimeSeriesWriter(f'{outF}.xdmf') as w:

        w.write_points_cells(points,cells)

        for f in range(nf):
            pdata = {
                      'X': coord + displ[f,...],
                      'U': displ[f,...],
                    }
            cdata = {
                     'LE': [strain[f,...]],
                      'S': [stress[f,...]],
                    }
            for i in range(nvfs):
                cdata[f'VF{i+1}'] = [vfs['e'][i,...]]

            w.write_data(f,point_data=pdata,cell_data=cdata)

    # Move .h5 file from cwd to output folder
    shutil.move(f'{out}.h5',f'{outF}.h5')

    return