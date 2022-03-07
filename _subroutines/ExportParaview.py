import os
import shutil
import meshio
import numpy as np

def ExportParaview(coord,conn,displ,strain,stress,ne,dof,nf,out):
    """
    Export experimental finite element mesh to paraview file.

    Parameters
    ----------
    eFEM : dict
        Final experimental finite element mesh dict.
    dir : str
        Directory of project to export output files.
    """

    # Transform strain into 3d tensor with zero values on 3d components
    if dof == 2:
        strain3d = np.zeros((nf,ne,6))
        stress3d = np.zeros((nf,ne,6))
        strain3d[...,[0,1,3]] = strain
        stress3d[...,[0,1,3]] = stress


    # Swap out-of-plane shear components for paraview notation
    if dof == 3:
        strain3d = strain[...,[0,1,2,3,5,4]]
        stress3d = stress[...,[0,1,2,3,5,4]]

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
            w.write_data(f,
            point_data = {
                             'X': coord + displ[f,...],
                             'U': displ[f,...],
                         },
            cell_data  = {
                            'LE': [strain3d[f,...]],
                             'S': [stress3d[f,...]],
                         }
                        )

    # Move .h5 file from cwd to output folder
    shutil.move(f'{out}.h5',f'{outF}.h5')

    return