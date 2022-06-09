import numpy as np

def hydrostatic_stress(stress):
    """
    Compute the hydrostatic stress in global csys.

    Parameters
    ----------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.

    Returns
    -------
    hydstress : (nf,ne) , float
        Hydrostatic stress in global csys.

    Notes
    -----
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nf : int
        Number of increments.
    """

    hydstress = 1/3 * np.trace(stress,axis1=2,axis2=3)

    return hydstress