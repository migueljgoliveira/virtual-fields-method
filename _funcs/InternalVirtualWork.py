import numpy as np

import _funcs
import _utils

def internal_virtual_work(strain,rot,dfgrd,rotm,vol,vfs,ne,dof,ndi,nshr,ntens,
                          nstatev,nvfs,nf,nprops,props,nlgeom,fout):
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
    vol : (ne),float
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
    nprops : int
        Number of material properties.
    props : (nprops) , float
        Material properties.
    nlgeom : bool
        Flag for small or large deformation framework (False/True).
    fout : str
        Name of output folder.

    Returns
    -------
    ivw : (nvfs,nf) , float
        Internal virtual work.
    success : bool
        Variable to monitor the sucess of stress reconstruction (False/True).
    """

    # Compute cauchy stress on global csys
    stress,_,de33,success = _funcs.cauchy_stress(strain,rot,rotm,ne,dof,ndi,
                                                 nshr,ntens,nstatev,nf,nprops,
                                                 props,fout)

    # # Compute hydrostatic stress on global csys
    # hydstress = _funcs.hydrostatic_stress(stress)

    # # Compute deviatoric stress on global csys 
    # devstress = _funcs.deviatoric_stress(stress,hydstress,dof)

    # Large deformation formulation
    if nlgeom:

        # Compute 1st piola-kirchhoff stress
        pkstress = _funcs.piola_kirchhoff_stress(stress,de33,dfgrd,ne,dof,nf)

        # Compute internal virtual work
        ivw = pkstress[None] * vfs * vol[None,None,:,None]

        # Sum internal virtual work along ne and ncomp
        ivw = np.nansum(ivw,(2,3))

    # Small deformation formulation
    else:

        # Transform cauchy stress tensor to voigt notation
        stress = _utils.tensor_to_voigt(stress,ne,ndi,ntens,nf)

        # Transform virtual fields tensor to voigt notation
        vfs = _utils.tensor_to_voigt(vfs,ne,ndi,ntens,nvfs)

        # Compute internal virtual work
        ivw = stress[:,None] * vfs[None] * vol[None,None,:,None]

        # Sum internal virtual work along ne and ntens
        ivw = np.nansum(ivw,(2,3))

    return ivw,success