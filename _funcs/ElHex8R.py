import numpy as np

def el_hex8r(coord):
    """
    8-Node hexahedral element w. reduced integration.

    Parameters
    ----------
    coord : (ne,8,3) , float
        Nodes reference coordinates.

    Returns
    -------
    dNdnr : (ne,3,8) , float
        Partial derivatives of shape function wrt natural coordinates.
    jac : (ne,3,3) , float
        Jacobian matrix.
    vol : (ne,) , float
        Element volume.

    Notes
    -----
    ne : int
        Number of elements.
    """

    # Partial derivatives of shape function wrt natural coordinates.
    dNdnr = np.array([[ -1,  1,  1, -1, -1,  1,  1, -1 ],
                      [ -1, -1, -1, -1,  1,  1,  1,  1 ],
                      [  1,  1, -1, -1,  1,  1, -1, -1 ]]) / 8

    # Jacobian matrix --> partial derivatives of cartesian wrt natural
    jac = dNdnr @ coord

    # Elements volume in reference configuration
    vol = abs(np.linalg.det(jac) * 8.0)

    return dNdnr,jac,vol