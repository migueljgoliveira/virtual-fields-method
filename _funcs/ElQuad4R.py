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
    dndnr : (ne,4,2) , float
        Shape function derivatives wrt natural coordinates.
    jac : (ne,2,2) or (nf,ne,2,2), float
        Elements jacobian matrix.
    vol : (ne,) , float
        Element volume.

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

          dndnr_xi =   xi * (1+eta*eta0)/4
         dndnr_eta =  eta *   (1+xi*xi0)/4
    """

    # Shape function derivatives wrt natural coordinates
    dndnr = np.array([[-1,-1],
                      [ 1,-1],
                      [ 1, 1],
                      [-1, 1]])/4

    # Elements jacobian matrix
    jac = np.transpose(coord,(0,2,1)) @ dndnr

    # Elements volume in reference configuration
    vol = abs(thick * np.linalg.det(jac) * 4.0)

    return dndnr,jac,vol