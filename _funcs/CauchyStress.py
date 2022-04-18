import _funcs

def cauchy_stress(strain,rot,rotm,ne,dof,ndi,nshr,ntens,nstatev,nf,nprops,
                  props,fout,voigt=0):
    """
    Compute the cauchy stress in local csys using the backward-Euler with an elastic predictor and plastic corrector.

    Parameters
    ----------
    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    rotm : (dof,dof) , float
        Material rotation tensor.
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
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Material properties.
    fout : str
        Name of output folder.
    voigt : bool
        Flag for voigt notation (0/1).

    Returns
    -------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.
    statev : (nf,ne,ntens+1) , float
        Internal state variables in global csys.
    de33 : (nf,ne) , float
        Strain in thickness direction.
    """

    # Stress integration in corotational material csys
    stress,statev,de33  = _funcs.ummdp(strain,ne,ndi,nshr,ntens,nstatev,
                                       props,nprops,nf,fout)

    # Rotate cauchy stress to global csys and convert to tensor form
    stress = _funcs.rotate_tensor(stress,rot,rotm,ne,dof,ndi,nshr,ntens,nf,
                                  dir=1,voigt=voigt)

    # Rotate statev to global csys
    statev[...,1:] = _funcs.rotate_tensor(statev[...,1:],rot,rotm,ne,dof,ndi,
                                          nshr,ntens,nf,dir=1,voigt=1,eng=1)

    return stress,statev,de33