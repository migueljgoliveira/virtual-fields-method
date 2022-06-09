import numpy as np

def material_rotation(ori,dof):
    """
    Compute material rotation tensor.

    Parameters
    ----------
    ori : float
        Material orientation angle in degrees.
    dof : int
        Number of degrees of freedom.

    Returns
    -------
    rotm : (dof,dof) ,float
        Material rotation tensor.
    """

    theta = np.radians(ori)
    c,s = np.cos(theta),np.sin(theta)
    rotm = np.array([[c,-s,0],[s,c,0],[0,0,1]])[:dof,:dof]

    rotm[abs(rotm) < 1e-16] = 0

    return rotm