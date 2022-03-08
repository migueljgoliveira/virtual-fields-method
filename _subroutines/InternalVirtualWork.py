import numpy as np
import _subroutines

def InternalVirtualWork(strain,rot,dfgrd,rotm,vol,vfs,props,nprops,
                        ne,dof,ndi,nshr,ntens,nstatev,nf,nlgeom=0):
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
    nf : int
        Number of increments.
    nlgeom : bool
        Flag for small/large deformation framework (0/1).

    Returns
    -------
    ivw : (nf,nvfs) , float
        Internal virtual work.
    Notes
    -----
    nvfs : int
        Number of virtual fields.
    """

    # Compute cauchy stress on corotational material csys
    stress,d33 = _subroutines.CauchyStress(strain,props,nprops,ne,ndi,
                                           nshr,ntens,nstatev,nf)

    # Rotate cauchy stress to global csys
    stress = _subroutines.RotateTensor(stress,rot,rotm,ne,dof,ndi,nshr,
                                       ntens,nf,dir=1,voigt=0)

    # Select small or large deformation framework
    if nlgeom:
        # Compute 1st piola-kirchhoff stress on global csys
        pkstress = _subroutines.PiolaKirchhoffStress(stress,d33,dfgrd,dof)

        # Compute internal virtual work
        ivw = pkstress[:,None] * vfs[None] * vol[None,None,:,None,None]
    else:
        # Compute internal virtual work
        ivw = stress[:,None] * vfs[None] * vol[None,None,:,None,None]

    # Sum internal virtual work along ne and dof
    ivw = np.sum(ivw,(2,3,4))

    return ivw