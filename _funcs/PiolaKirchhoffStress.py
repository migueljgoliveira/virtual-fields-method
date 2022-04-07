import numpy as np

def piola_kirchhoff_stress(stress,de33,dfgrd):
    """ 
    Compute the 1st Piola-Kirchhoff stress.

    Parameters
    ----------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.
    de33 : (nf,ne) , float
        Strain in thickness direction.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.

    Returns
    -------
    pkstress : (nf,ne,dof,dof) , float
        1st piola-kirchhoff stress.

    Notes
    -----
    nf : int
        Number of increments.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    """

    # Determinant of deformation gradient
    dfgrddet = (1 + de33) * np.linalg.det(dfgrd)

    # Transpose of inverse of deformation gradient
    dfgrdinvt = np.transpose(np.linalg.inv(dfgrd),(0,1,3,2))

    # 1st piola-kirchhoff stress
    pkstress = dfgrddet[...,None,None] * stress @ dfgrdinvt

    return pkstress