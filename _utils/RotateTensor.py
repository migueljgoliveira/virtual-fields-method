import numpy as np

import _utils

def rotate_tensor(array,rot,rotm,ne,dof,ndi,ntens,nf,dir,voigt=True,eng=False):
    """
    Rotate tensor from global to corotational material csys and vice-versa.

    Parameters
    ----------
    array : (nf,ne,ntens) , float or (nf,ne,dof,dof) , float
        Array, either voigt or tensor form.
    rot : (nf,ne,dof,dof) , float
        Rigid-body rotation tensor.
    rotm : (dof,dof) , float
        Material rotation tensor.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    ndi : int
        Number of normal tensor components.
    ntens : int
        Number of tensor components.
    nf : int
        Number of increments.
    dir : int
        Flag for material corotational/global csys (-1/1).
    voigt : bool
        Flag for voigt notation (False/True).
    eng : bool
        Flag for engineering strain (False/True).

    Returns
    -------
    arrayR : (nf,ne,ntens) or (nf,ne,dof,dof) , float
        Rotated array, either voigt or tensor form.
    """

    # Convert voigt to tensor form if necessary
    if len(array.shape) == 3:
        array = _utils.voigt_to_tensor(array,ne,dof,ntens,nf,eng)

    # Rotate to material corotational csys
    if dir == -1:
        arrayR = rotm.T @ (np.transpose(rot,(0,1,3,2)) @ array @ rot) @ rotm

    # Rotate to global csys
    elif dir == 1:
        arrayR = rotm @ (rot @ array @ np.transpose(rot,(0,1,3,2))) @ rotm.T

    # Convert to voigt notation if requested
    if voigt:
        arrayR = _utils.tensor_to_voigt(arrayR,ne,ndi,ntens,nf,eng)

    return arrayR