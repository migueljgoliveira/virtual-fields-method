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
    dNdNr : (ne,3,8) , float
        Shape function derivatives wrt natural coordinates.
    jac : (ne,3,3) , float
        Jacobian matrix.
    vol : (ne,) , float
        Element volume.

    Notes
    -----
    ne : int
        Number of elements.

    Theory
    ------
    Vectors of natural coordinates xi, eta, and zeta are equal to

          xi = [-1, 1, 1,-1,-1, 1, 1,-1],
         eta = [-1,-1,-1,-1, 1, 1, 1, 1],
        zeta = [ 1, 1,-1,-1, 1, 1,-1,-1],

    and the integration point has natural coordinates

          xi0 = 0,
         eta0 = 0,
        zeta0 = 0. 

    The shape function derivatives wrt natural coordinates will be equal to

          dNdNr_xi =   xi * (1+eta*eta0)*(1+zeta*zeta0) /8
         dNdNr_eta =  eta *   (1+xi*xi0)*(1+zeta*zeta0) /8
        dNdNr_zeta = zeta *   (1+xi*xi0)*  (1+eta*eta0) /8

    """

    # Shape function derivatives wrt natural coordinates
    dNdNr = np.array([[-1, 1, 1,-1,-1, 1, 1,-1],
                      [-1,-1,-1,-1, 1, 1, 1, 1],
                      [ 1, 1,-1,-1, 1, 1,-1,-1]])/8

    # Jacobian matrix
    jac = dNdNr @ coord

    # Element volume
    vol = abs(np.linalg.det(jac)*8.0)

    return dNdNr,jac,vol