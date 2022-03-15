import numpy as np

import _funcs

def internal_virtual_work(strain,rot,dfgrd,rotm,vol,vfs,ne,dof,ndi,nshr,ntens,
                          nstatev,nvfs,nf,nlgeom,props,nprops):
    """
    Compute the internal virtual work.

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
    vol : (ne,),float
        Elements volume.
    vfs : (nvfs,ne,dof,dof) , float
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
    """

    # Compute cauchy stress on global csys
    stress,_,d33 = _funcs.cauchy_stress(strain,rot,rotm,ne,dof,ndi,nshr,ntens,
                                        nstatev,nf,props,nprops,voigt=0)

    # Large deformation framework
    if nlgeom:

        # Compute 1st piola-kirchhoff stress
        pkstress = _funcs.piola_kirchhoff_stress(stress,d33,dfgrd,dof)

        # Compute internal virtual work
        ivw = pkstress[:,None] * vfs[None] * vol[None,None,:,None,None]

        # Sum internal virtual work along ne and dof
        ivw = np.nansum(ivw,(2,3,4))

    # Small deformation framework
    else:

        # Transform cauchy stress tensor to voigt notation
        stress = _funcs.tensor_to_voigt(stress,ne,ndi,ntens,nf)

        # Transform virtual fields tensor to voigt notation
        vfs = _funcs.tensor_to_voigt(vfs,ne,ndi,ntens,nvfs)

        # Compute internal virtual work
        ivw = stress[:,None] * vfs[None] * vol[None,None,:,None]

        # Sum internal virtual work along ne and ntens
        ivw = np.nansum(ivw,(2,3))

    return ivw