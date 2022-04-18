import numpy as np

def el_quad4r(coord,thick):
    """
    4-Node quadrilateral element w. reduced integration.

    Parameters
    ----------
    coord : (ne,4,2) , float
        Nodes reference coordinates.
    thick : float
        Specimen initial thickness.

    Returns
    -------
    dNdnr : (ne,4,2) , float
        Partial derivatives of shape function wrt natural coordinates.
    jac : (ne,2,2) , float
        Jacobian matrix.
    vol : (ne,) , float
        Element volume.

    Notes
    -----
    ne : int
        Number of elements.
    """

    # Partial derivatives of shape function wrt natural coordinates
    dNdnr = np.array([[-1, 1, 1,-1],
                      [-1,-1, 1, 1]])/4

    # Jacobian matrix --> partial derivatives of cartesian wrt natural
    jac = dNdnr @ coord

    # Elements volume in reference configuration
    vol = abs(thick * np.linalg.det(jac) * 4.0)

    return dNdnr,jac,vol