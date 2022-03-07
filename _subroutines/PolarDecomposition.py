import numpy as np

def PolarDecomposition(dfgrd,side='left'):
    """
    Perform the polar decomposition of the deformation gradient.

    Parameters
    ----------
    dfgrd : (nf,ne,dof,dof),float
        Deformation gradient.

    Returns
    -------
    rot : (nf,ne,dof,dof),float
        Rigid-body rotation tensor.
    strch : (nf,ne,dof,dof),float
        Deformation left or right stretch tensor.

    Notes
    -----
    nf : int
        Number of increments.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.

    See Also
    --------
    scipy.linalg.polar : compute the polar decomposition of a single
      matrix.

    Theory
    ------
    The deformation gradient F can be written as
        F = VR or F = UR,
      where V is the left-stretch tensor and U is the right-stretch
      tensor. U is the stretch tensor on the global csys and V is the
      stress tensor on the local csys. This way, U can be said to be
      the stretch tensor free of rigid-body rotations, so that the
      relationship between V and U is given by U = R'UR.
    """

    # Singular value decomposition of deformation gradient
    W,S,Vh = np.linalg.svd(dfgrd,full_matrices=False)

    # Rotation tensor
    rot = W @ Vh

    # Left stretch tensor
    if side == 'left':
        strch = (W * S[:,:,None,:]) @ np.transpose(W,(0,1,3,2))

    # Right stretch tensor
    elif side == 'right':
        strch = (np.transpose(Vh,(0,1,3,2)) * S[:,:,None,:]) @ Vh

    return rot,strch