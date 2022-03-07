import numpy as np

def ElQuad4R(coord):
    """
    4-Node quadrilateral element w. reduced integration.

    Parameters
    ----------
    coord : (ne,4,2),float
        Nodes reference coordinates.

    Returns
    -------
    dNdNr : (ne,2,4),float
        Shape function derivatives wrt natural coordinates.
    jac : (ne,2,2),float
        Jacobian matrix.
    area : (ne,),float
        Element area.

    Notes
    -----
    ne : int
        Number of elements.

    Theory
    ------
    Vectors of natural coordinates xi, eta, and zeta are equal to

          xi = [-1, 1, 1,-1],
         eta = [-1,-1, 1, 1],

    and the integration point has natural coordinates

          xi0 = 0,
         eta0 = 0,

    The shape function derivatives wrt natural coordinates will be equal to

          dNdNr_xi =   xi * (1+eta*eta0)/4
         dNdNr_eta =  eta *   (1+xi*xi0)/4
    """

    # Shape function derivatives wrt natural coordinates
    dNdNr = np.array([[-1, 1, 1,-1],
                      [-1,-1, 1, 1]])/4

    # Jacobian matrix
    jac = dNdNr @ coord

    # element area
    area = np.linalg.det(jac)*4.0

    return dNdNr,jac,area