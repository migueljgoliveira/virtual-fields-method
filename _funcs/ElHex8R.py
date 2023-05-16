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

    Nodes Numbering : Element of Size 2

                                    ( x, y, z)
        4---------1           O --> ( 0, 0, 1)
        |         |      Node 1 --> ( 1, 1, 1)
        |    O    |      Node 2 --> ( 1,-1, 1)
        |         |      Node 3 --> (-1, 1, 1)
        3---------2      Node 4 --> (-1,-1, 1)

                                    ( x, y, z)
        8---------5           O --> ( 0, 0,-1)
        |         |      Node 5 --> ( 1, 1,-1)
        |    O    |      Node 6 --> ( 1,-1,-1)
        |         |      Node 7 --> (-1, 1,-1)
        7---------6      Node 8 --> (-1,-1,-1)
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