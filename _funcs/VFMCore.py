import numpy as np

import _funcs

def vfm_core(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,
             nstatev,nvfs,nf,nprops,props,nlgeom,fout):
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
    vfs : {(nvfs,nf,ne,dof,dof), (nvfs,nf,nn,dof)} , float
        Settings and generated virtual fields.
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
    res : (nvfs*nf) , float
        Cost function residuals for time increments and virtual fields.
    phi : float
        Cost function.
    success : bool
        Variable to monitor the sucess of stress reconstruction (False/True).
    """

    # Compute internal virtual work
    ivw,success = _funcs.internal_virtual_work(strain,rot,dfgrd,rotm,vol,
                                               vfs['e'],ne,dof,ndi,nshr,ntens,
                                               nstatev,nvfs,nf,nprops,props,
                                               nlgeom,fout)

    # Compute external virtual work
    evw = _funcs.external_virtual_work(force,vfs['u'])

    # Compute scaling parameter
    if 'sb' in list(vfs.keys()):
        alpha = _funcs.scaling_virtual_fields(ivw,vfs['sb']['scale'],nf)
    else:
        alpha = np.ones((nvfs,1))

    # Compute residuals of increments and virtual fields
    res = np.ravel(alpha * (ivw - evw),order='F')

    # Compute cost function
    phi = np.sum(res**2)

    return ivw,evw,phi,success