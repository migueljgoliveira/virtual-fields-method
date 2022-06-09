import numpy as np

def deviatoric_stress(stress,hydstress,dof):
    """
    Compute the deviatoric stress in global csys.

    Parameters
    ----------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.
    hydstress : (nf,ne) , float
        Hydrostatic stress in global csys.

    Returns
    -------
    devstress : (nf,ne,dof,dof) , float
        Deviatoric stress in global csys.

    Notes
    -----
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nf : int
        Number of increments.
    """

    devstress = stress - hydstress[...,None,None] * np.identity(dof)[None,None]

    return devstress