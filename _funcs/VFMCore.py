import numpy as np

import _funcs

def vfm_core(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,nstatev,
             nvfs,nf,symm,nprops,props,nlgeom,fout):
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
    symm : (nsymm,), int
        List of symmetry conditions.
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Material properties.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).

    fout : str
        Name of output folder.

    Returns
    -------
    ivw : (nvfs,nf) , float
        Internal virtual work.
    evw : (nvfs,nf) , float
        External virtual work.
    res : (nvfs*nf,) , float
        Cost function residuals for time increments and virtual fields.
    phi : float
        Cost function.
    """

    # Compute internal virtual work
    ivw = _funcs.internal_virtual_work(strain,rot,dfgrd,rotm,vol,vfs['e'],ne,
                                       dof,ndi,nshr,ntens,nstatev,nvfs,nf,
                                       nprops,props,nlgeom,symm,fout)

    # Compute external virtual work
    evw = _funcs.external_virtual_work(force,vfs['u'])

    # Compute residuals of increments and virtual fields
    res = np.ravel(ivw - evw,order='F')

    # Compute cost function
    phi = 0.5*np.sum(res**2)

    return ivw,evw,res,phi