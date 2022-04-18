import os
import shutil
import meshio
import numpy as np

def export_paraview(coord,displ,conn,strain,vol,stress,peeq,pstrain,de33,
                    pkstress,vfs,dof,nvfs,nf,test,nt,out,folder='output'):
    """
    Export experimental finite element mesh to paraview file.

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    displ : (nf,nn,dof) , float
        Nodes displacements.
    conn : (ne,npe) , int
        Elements connectivity.
    strain : (nf,ne,ntens) , float
        Strain in global csys.
    stress : (nf,ne,ntens) , float
        Cauchy stress in global csys.
    peeq : (nf,ne) , float
        Equivalent plastic strain.
    pstrain : (nf,ne,ntens) , float
        Plastic strain in global csys.
    de33 : (nf,ne) , float
        Strain in thickness direction.
    pkstress : (nf,ne,dof,dof) , float
        1st piola-kirchhoff stress.
    vfs : {(nvfs,ne,dof,dof), (nvfs,nn,dof)} , float
        User defined virtual fields.
    dof : int
        Number of degrees of freedom.
    nvfs : int
        Number of virtual fields.
    nf : int
        Number of increments.
    test : str
        Name of test.
    nt : int
        Number of tests.
    out : str
        Name of output folder.
    folder : str
        Type of export folder.

    Notes
    -----
    ne : int
        Number of elements.
    """

    # Nodes and elements connectivity
    points = coord
    if dof == 2:
        cells = [('quad',conn)]
    elif dof == 3:
        cells = [('hexahedron',conn)]

    # Set output folder
    if nt > 1:
        outF = f'{os.getcwd()}\\{folder}\\{out}\\{test}\\{test}'
    else:
        outF = f'{os.getcwd()}\\{folder}\\{out}\\{out}'

    # Output paraview file
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
                   'PEEQ': [peeq[f,...]],
                     'PE': [pstrain[f,...]],
                     'PK': [pkstress[f,...]],
                    'VOL': [vol],
                    }

            # Add virtual strain fields
            if (folder == 'output'):
                for i in range(nvfs):
                    cdata[f'VF{i+1}'] = [vfs['e'][i,f,...]]

            # Add thickness strain
            if dof == 2:
                cdata['de33'] = [de33[f,...]]

            # Write data
            w.write_data(f,point_data=pdata,cell_data=cdata)

    # Move .h5 file from cwd to output folder
    if nt > 1:
        shutil.move(f'{test}.h5',f'{outF}.h5')
    else:
        shutil.move(f'{out}.h5',f'{outF}.h5')

    return