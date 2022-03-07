import numpy as np

def DeformationGradient(displ,dNdNr,jac,dof):
    """ 
    Compute the deformation gradient.

    Parameters
    ----------
    displ : (nf,ne,npe,dof),float
        Nodes displacements.
    dNdNr : (dof,npe),float
        Shape function derivatives wrt natural  coordinates.
    jac : (ne,dof,dof),float
        Jacobian matrix.
    dof : int
        Number of degrees of freedom.

    Returns
    -------
    dfgrd : (nf,ne,dof,dof),float
        Deformation gradient.

    Notes
    -----
    nf : int
        Number of increments.
    ne : int
        Number of elements.
    npe : int
        Number of nodes per element.
    """

    # Derivatives of shape functions wrt. cartesian coordinates
    dNdX = np.linalg.inv(jac) @ dNdNr

    # Deformation gradient
    dUdX = dNdX @ displ
    dfgrd = np.identity(dof) + dUdX

    return dfgrd