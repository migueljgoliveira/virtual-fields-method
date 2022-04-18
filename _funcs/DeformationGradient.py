import numpy as np

def deformation_gradient(displ,dNdnr,jac,dof):
    """ 
    Compute the deformation gradient.

    Parameters
    ----------
    displ : (nf,ne,npe,dof) , float
        Nodes displacements.
    dNdnr : (npe,dof) , float
        Partial derivatives of shape function wrt natural coordinates.
    jac : (ne,dof,dof) or (nf,ne,dof,dof), float
        Jacobian matrix.
    dof : int
        Number of degrees of freedom.

    Returns
    -------
    dfgrd : (nf,ne,dof,dof) , float
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

    # Partial derivatives of displacements wrt natural coordinates
    dUdNr = dNdnr @ displ

    # Inverse of jacobian matrix
    dNrdX = np.linalg.inv(jac)

    # Partial derivatives of displacements wrt cartesian coordinates
    dUdX = dNrdX @ dUdNr

    # Deformation gradient
    dfgrd = np.identity(dof) + np.transpose(dUdX,(0,1,3,2))

    return dfgrd