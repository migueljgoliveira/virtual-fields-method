import numpy as np

def polar_decomposition(dfgrd,dof,side='left'):
    """
    Perform the polar decomposition of the deformation gradient.

    Parameters
    ----------
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    dof : int
        Number of degrees of freedom.

    Returns
    -------
    rot : (nf,ne,dof,dof) , float
        Rigid-body rotation tensor.
    strch : (nf,ne,dof,dof) , float
        Deformation left or right stretch tensor.

    Notes
    -----
    nf : int
        Number of increments.
    ne : int
        Number of elements.

    See Also
    --------
    scipy.linalg.polar : compute the polar decomposition of a single
      matrix.

    Theory
    ------
    The deformation gradient F can be written as
        F = VR or F = RU,
      where V is the left-stretch tensor and U is the right-stretch
      tensor. V is the stretch tensor on the global csys and U is the
      stretch tensor on the corotational csys. This way, U can be said to be
      the stretch tensor free of rigid-body rotations, so that the
      relationship between V and U is given by U = R'VR.
    """

    # Singular value decomposition of deformation gradient
    W,S,Vh = np.linalg.svd(dfgrd,full_matrices=False)

    # Left stretch tensor V and rotation tensor R
    if side == 'left':
        strch = (W * S[...,None,:]) @ np.transpose(W,(0,1,3,2))
        rot = np.linalg.inv(strch) @ dfgrd

    # Right stretch tensor U and rotation tensor R
    elif side == 'right':
        strch = (np.transpose(Vh,(0,1,3,2)) * S[...,None,:]) @ Vh
        rot = dfgrd @ np.linalg.inv(strch)

    return rot,strch