import numpy as np

import _subroutines

def VFMCore(strain,rot,dfgrd,rotm,force,vol,vfs,props,
            nprops,ne,dof,ndi,nshr,ntens,nstatev,nvfs,nf,nlgeom):
    """
    VFM Core Function

    Parameters
    ----------
    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    rotm : (dof,dof) , float
        Material rotation tensor.
    force : (nf,dof) , float
        Global loading force.
    vol : (ne,) , float
        Elements volume.
    vfs : {(nvfs,ne,dof,dof), (nvfs,nn,dof)} , float
        User defined virtual fields.
    props : (nprops,) , float
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
    nvfs : int
        Number of virtual fields.
    nf : int
        Number of increments.
    nlgeom : bool
        Flag for small/large deformation framework (0/1).

    Returns
    -------
    """

    # Compute internal virtual work
    ivw = _subroutines.InternalVirtualWork(strain,rot,dfgrd,rotm,vol,vfs['e'],
                                           props,nprops,ne,dof,ndi,nshr,
                                           ntens,nstatev,nf,nlgeom)

    # Compute external virtual work
    evw = _subroutines.ExternalVirtualWork(force,vfs['u'])

    # Compute residuals of increments and virtual fields
    res =  np.ravel((ivw - evw)**2)

    # Compute cost function
    phi = np.sum(res)/(nf*nvfs)

    return phi