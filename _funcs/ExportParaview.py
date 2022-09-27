import os
import shutil
import meshio
import numpy as np
from scipy.fftpack import ss_diff

import _utils

def export_paraview(coord,displ,conn,strain,vol,stress,peeq,pstrain,de33,
                    pkstress,vfs,ss,iss,ne,dof,nvfs,nf,test,nt,fout,dirout,vfsu):
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
    vfs : {(nvfs,nf,ne,dof,dof), (nvfs,nf,nn,dof)} , float
        Settings and generated virtual fields.
    ss : (nvfs,nf,ne,dof,dof) or None , float
        Total stress sensitivity.
    iss : (nvfs,nf,ne,dof,dof) or None , float
        Incremental stress sensitivity.
    ne : int
        Number of elements.
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
    fout : str
        Name of output folder.
    dirout : str
        Directory of project to export output files.
    """

    # Rearrange voigt components
    if dof == 2:
        stress3d = np.zeros((nf,ne,6))
        strain3d = np.zeros((nf,ne,6))
        pstrain3d = np.zeros((nf,ne,6))

        stress3d[...,[0,1,3]] = stress
        strain3d[...,[0,1,3]] = strain
        pstrain3d[...,[0,1,3]] = pstrain

    elif dof == 3:
        stress3d = stress[...,[0,1,2,3,5,4]]
        strain3d = strain[...,[0,1,2,3,5,4]]
        pstrain3d = pstrain[...,[0,1,2,3,5,4]]

    # Rearrange tensor components for paraview export
    pkstress = _utils.rearrange_tensor(pkstress,ne,dof,nf)[0,...]

    if 'sb' in list(vfs.keys()):
        ss = _utils.rearrange_tensor(ss,ne,dof,nf,nvfs)
        iss = _utils.rearrange_tensor(iss,ne,dof,nf,nvfs)

    # Repeat user-defined virtual fields over time increments
    if 'ud' in list(vfs.keys()):
        vfs['e'] = np.repeat(vfs['e'],nf,1)

        vfsu = np.repeat(vfsu,nf,1)

    # Reshape virtual fields to tensor format
    vfs['e'] = np.reshape(vfs['e'],(nvfs,nf,ne,dof,dof))

    # Nodes and elements connectivity
    points = coord
    if dof == 2:
        cells = [('quad',conn)]
    elif dof == 3:
        cells = [('hexahedron',conn)]

    # Set output folder
    if nt > 1:
        outF = os.path.join(dirout,fout,test)
    else:
        outF = os.path.join(dirout,fout)

    # Output paraview file
    with meshio.xdmf.TimeSeriesWriter(f'{outF}.xdmf') as w:

        w.write_points_cells(points,cells)

        for f in range(nf):
            pdata = {
                      'X': coord + displ[f,...],
                      'U': displ[f,...],
                    }
            cdata = {
                     'LE': [strain3d[f,...]],
                      'S': [stress3d[f,...]],
                   'PEEQ': [peeq[f,...]],
                     'PE': [pstrain3d[f,...]],
                     'PK': [pkstress[f,...]],
                    'VOL': [vol],
                    }

            # Add virtual displacement fields
            for i in range(nvfs):
                pdata[f'VF{i+1}'] = vfsu[i,f,...]

            # Add virtual strain fields
            for i in range(nvfs):
                cdata[f'VF{i+1}'] = [vfs['e'][i,f,...]]

            # Add stress sensitivities
            if 'sb' in list(vfs.keys()):
                for i in range(nvfs):
                    cdata[f'SS{i+1}'] = [ss[i,f,...]]
                    cdata[f'ISS{i+1}'] = [iss[i,f,...]]

            # Add thickness strain
            if dof == 2:
                cdata['de33'] = [de33[f,...]]

            # Write data
            w.write_data(f,point_data=pdata,cell_data=cdata)

    # Move .h5 file from cwd to output folder
    if nt > 1:
        shutil.move(f'{test}.h5',f'{outF}.h5')
    else:
        shutil.move(f'{fout}.h5',f'{outF}.h5')

    return