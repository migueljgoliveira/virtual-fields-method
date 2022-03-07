import numpy as np

import _subroutines
from ummdp_vfm import ummdp_vfm

def VFM(name,out):

    # Create output directory
    _subroutines.CreateDirectory(out)

    # Load geometry data
    coord,displ,conn,force,nf = _subroutines.LoadData(name)

    # Load material properties
    props,nprops = _subroutines.MaterialProperties()

    # Set dimensional variables
    nn,ne,npe,dof,ndi,nshr,ntens,nstatev = _subroutines.DimVars(coord,conn)

    # Compute material rotation tensor
    rotm = _subroutines.MaterialRotation(0,dof)

    # Compute strain and deformation gradient
    strain,rot,dfgrd = _subroutines.LogStrain(coord[conn],displ[:,conn],rotm,
                                              ne,npe,dof,ndi,nshr,ntens,nf)

    stress = _subroutines.VFMCore(strain,rot,dfgrd,rotm,force,
                                  props,nprops,
                                  ne,dof,ndi,nshr,ntens,nstatev,nf)


    # Export model to paraview
    # _subroutines.ExportParaview(coord,conn,displ,strain,stress,ne,dof,nf,out)

    return

if __name__ == '__main__':
    
    name = '9elem-distload-elastic'
    output = '9elem-distload-elastic'

    VFM(name,output)