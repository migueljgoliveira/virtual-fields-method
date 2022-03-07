import numpy as np

import _subroutines

def VFMCore(strain,rot,dfgrd,rotm,force,
            props,nprops,
            ne,dof,ndi,nshr,ntens,nstatev,nf):
    """
    VFM Core Function

    Parameters
    ----------
    strain : (nf,ne,ntens),float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof),float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof),float
        Deformation gradient.
    rotm : (dof,dof),float
        Material rotation tensor.
    force : (nf,dof),float
        Global external force.
    props : (nprops,),float
        Material properties.
    nprops : int
        Number of material properties.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    ndi : int
        Number of normal tensor components.
    nshr : int
        Number of shear tensor components.
    ntens : int
        Number of tensor components.
    nstatev : int
        Number of internal state variables.
    nf : int
        Number of increments.

    Returns
    -------
    """

    # Compute internal virtual work
    ivw = _subroutines.InternalVirtualWork()

    # Compute external virtual work
    evw = _subroutines.ExternalVirtualWork(force)



    # return stress