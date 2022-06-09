import numpy as np

import _utils

def piola_kirchhoff_stress(stress,de33,dfgrd,ne,dof,nf,flat=True):
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
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nf : int
        Number of increments.
    flat : bool
        Flag to flatten tensor (False/True).

    Returns
    -------
    pkstress : (nf,ne,dof*dof) , float
        1st piola-kirchhoff stress.
    """

    # Determinant of deformation gradient
    dfgrddet = (1 + de33) * np.linalg.det(dfgrd)

    # Transpose of inverse of deformation gradient
    dfgrdinvt = np.transpose(np.linalg.inv(dfgrd),(0,1,3,2))

    # 1st piola-kirchhoff stress
    pkstress = dfgrddet[...,None,None] * stress @ dfgrdinvt

    # Flatten 1st piola-kirchhoff stress and rearrange components order
    if flat:
        pkstress = _utils.flatten_tensor(pkstress,ne,dof,nf)

    return pkstress