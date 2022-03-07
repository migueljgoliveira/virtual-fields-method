import numpy as np

def MaterialRotation(theta,dof):
    """
    Compute material rotation tensor.

    Parameters
    ----------
    theta : float
        Material anisotropic angle in degrees.
    dof : int
        Number of degrees of freedom.

    Returns
    -------
    rotm : (3,3),float
        Material rotation tensor.
    """

    theta = np.radians(theta)
    c,s = np.cos(theta),np.sin(theta)
    rotm = np.array([[c,-s,0],[s,c,0],[0,0,1]])

    return rotm[:dof,:dof]