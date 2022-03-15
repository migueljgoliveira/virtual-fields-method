import numpy as np

import _funcs

def vfm_core(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,nstatev,
             nvfs,nf,nlgeom,props,nprops):
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
        Flag for small or large deformation framework (0/1).
    props : (nprops,) , float
        Material properties.
    nprops : int
        Number of material properties.

    Returns
    -------
    ivw : (nf,nvfs) , float
        Internal virtual work.
    evw : (nf,nvfs) , float
        External virtual work.
    res : (nf*nvfs,) , float
        Cost function residuals for time increments and virtual fields.
    phi : float
        Cost function.
    """

    # Compute internal virtual work
    ivw = _funcs.internal_virtual_work(strain,rot,dfgrd,rotm,vol,vfs['e'],ne,
                                       dof,ndi,nshr,ntens,nstatev,nvfs,nf,
                                       nlgeom,props,nprops)

    # Compute external virtual work
    evw = _funcs.external_virtual_work(force,vfs['u'])

    # Compute residuals of increments and virtual fields
    res = np.ravel((ivw - evw)**2)

    # Compute cost function
    phi = np.sum(res)/(nf*nvfs)

    return ivw,evw,res,phi