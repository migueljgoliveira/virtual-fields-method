import os
import shutil
import meshio
import numpy as np

def export_paraview(coord,displ,conn,strain,vol,stress,statev,d33,pkstress,vfs,
                    ne,dof,nvfs,nf,nt,out,test,folder='output'):
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
    statev : (nf,ne,ntens+1) , float
        Internal state variables in global csys.
    d33 : (nf,ne) , float
        Strain in thickness direction.
    pkstress : (nf,ne,dof,dof) , float
        1st piola-kirchhoff stress.
    vfs : {(nvfs,ne,dof,dof), (nvfs,nn,dof)} , float
        User defined virtual fields.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nvfs : int
        Number of virtual fields.
    nf : (nt,) , int
        Number of increments.
    nt : int
        Number of tests.
    out : str
        Name of output folder.
    test : str
        Name of test.
    folder : str
        Type of export folder.
    """

    # Swap out-of-plane shear components for paraview notation
    if dof == 3:
        strain = strain[...,[0,1,2,3,5,4]]
        stress = stress[...,[0,1,2,3,5,4]]
        statev[...,1:] = statev[...,[1,2,3,4,6,5]]

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
                   'PEEQ': [statev[f,...,0]],
                     'PE': [statev[f,...,1:]],
                     'PK': [pkstress[f,...]],
                    'VOL': [vol],
                    }

            # Add virtual strain fields
            if (folder == 'output'):
                for i in range(nvfs):
                    cdata[f'VF{i+1}'] = [vfs['e'][i,...]]

            # Add thickness strain
            if dof == 2:
                cdata['d33'] = [d33[f,...]]

            # Write data
            w.write_data(f,point_data=pdata,cell_data=cdata)

    # Move .h5 file from cwd to output folder
    if nt > 1:
        shutil.move(f'{test}.h5',f'{outF}.h5')
    else:
        shutil.move(f'{out}.h5',f'{outF}.h5')

    return