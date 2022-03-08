import numpy as np

import _subroutines
from ummdp_vfm import ummdp_vfm

def VFM(name,out):

    # Select small or large deformation framework
    nlgeom = 1

    # Create output directory
    _subroutines.CreateDirectory(out)

    # Load geometry data
    coord,displ,conn,centroid,force,thick,nf = _subroutines.LoadData(name)

    # Load material properties
    props,nprops = _subroutines.MaterialProperties()

    # Set dimensional variables
    nn,ne,npe,dof,ndi,nshr,ntens,nstatev = _subroutines.DimVars(coord,conn)

    # Compute material rotation tensor
    rotm = _subroutines.MaterialRotation(0,dof)

    # Compute strain and deformation gradient
    strain,rot,dfgrd,vol = _subroutines.LogStrain(coord[conn],displ[:,conn],
                                                  rotm,thick,ne,npe,dof,ndi,
                                                  nshr,ntens,nf)

    # Generate user defined virtual fields
    lvfs = np.array([1,2])
    nvfs = len(lvfs)
    vfs = _subroutines.UserDefinedVirtualFields(coord,centroid,nn,ne,
                                                dof,lvfs,nvfs)

    stress = _subroutines.VFMCore(strain,rot,dfgrd,rotm,force,vol,vfs,
                                  props,nprops,ne,dof,ndi,nshr,ntens,
                                  nstatev,nvfs,nf,nlgeom)


    # Export model to paraview
    _subroutines.ExportParaview(coord,conn,displ,strain,stress,
                                vfs,dof,nf,nvfs,out)

    return

if __name__ == '__main__':
    
    name = '9elem-distload-plastic'
    output = '9elem-distload-plastic'

    VFM(name,output)