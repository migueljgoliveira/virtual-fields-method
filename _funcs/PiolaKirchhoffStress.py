import numpy as np

def piola_kirchhoff_stress(stress,d33,dfgrd,dof):
    """ 
    Compute the 1st Piola-Kirchhoff stress.

    Parameters
    ----------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.
    d33 : (nf,ne) , float
        Strain in thickness direction.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    dof : int
        Number of degrees of freedom.

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
    """

    # Determinant of deformation gradient
    dfgrdDet = ((1 + d33) * np.linalg.det(dfgrd))

    # Transpose of deformation gradient inverse
    dfgrdInvT = np.transpose(np.linalg.inv(dfgrd),(0,1,3,2))

    # 1st piola-kirchhoff stress
    pkstress = dfgrdDet[...,None,None] * stress @ dfgrdInvT

    return pkstress