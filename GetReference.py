import os
import numpy as np

import _funcs
from ummdp_vfm import ummdp_vfm

def GetReference(name,out,lvfs,nlgeom=1):

    ##################
    # PRE-PROCESSING #
    ##################

    # Load geometry data
    coord,displ,conn,centroid,force,thick,ori,nf = _funcs.LoadData(name)

    # Load material properties
    props,nprops = _funcs.material_properties()

    # Set dimensional variables
    nn,ne,npe,dof,ndi,nshr,ntens,nstatev,nvfs = _funcs.dim_vars(coord,conn,
                                                                lvfs)

    # Compute material rotation tensor
    rotm = _funcs.material_rotation(ori,dof)

    # Compute strain and deformation gradient
    strain,rot,dfgrd,vol = _funcs.log_strain(coord[conn],displ[:,conn],rotm,
                                             thick,ne,npe,dof,ndi,nshr,
                                             ntens,nf)

    # Generate user defined virtual fields
    vfs = _funcs.user_defined_virtual_fields(coord,centroid,ne,dof,lvfs,nvfs)

    ##############
    # LOAD FORCE #
    ##############

    # Compute internal virtual work
    ivw = _funcs.internal_virtual_work(strain,rot,dfgrd,rotm,vol,vfs['e'],
                                       props,nprops,ne,dof,ndi,nshr,
                                       ntens,nstatev,nvfs,nf,nlgeom)

    # Compute load force
    force = ivw / 2

    ###################
    # POST-PROCESSING #
    ###################

    # Export reference force
    filename = f'input\{name}\{name}_Force.csv'
    oldforce = np.loadtxt(filename,skiprows=1,delimiter=';')
    oldforce[:,2] = force[:,0]
    os.rename(filename,f'input\{name}\{name}_ForceFEM.csv')
    with open(filename,'w') as f:
        if dof == 2:
            f.write('Time;X;Y\n')
        if dof == 3: 
            f.write('Time;X;Y;Z\n')
        np.savetxt(f,oldforce,delimiter=';')

    # Compute cauchy stress on corotational material csys in voigt form
    stress,statev,d33 = _funcs.cauchy_stress(strain,rot,rotm,props,nprops,ne,
                                             dof,ndi,nshr,ntens,nstatev,
                                             nf,voigt=1)

    # Rotate strain to global csys
    strain = _funcs.rotate_tensor(strain,rot,rotm,ne,dof,ndi,nshr,ntens,nf,
                                  dir=1,voigt=1,eng=0)

    # Export model to paraview
    _funcs.export_paraview(coord,displ,conn,strain,stress,statev,d33,vfs,dof,
                           nf,nvfs,out,folder='input')

    return

if __name__ == '__main__':

    name = 'Double-Notched-2D'
    output = name

    # Select small or large deformation framework (0/1)
    nlgeom = 1

    # Set type of user defined virtual fields
    lvfs = np.array([1])

    GetReference(name,output,lvfs,nlgeom)