import numpy as np

def deformation_gradient(displ,dndnr,jac,dof):
    """ 
    Compute the deformation gradient.

    Parameters
    ----------
    displ : (nf,ne,npe,dof) , float
        Nodes displacements.
    dndnr : (npe,dof) , float
        Shape function derivatives wrt natural  coordinates.
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

    # Derivatives of shape functions wrt. cartesian coordinates
    dndx = dndnr @ np.linalg.inv(jac)

    # Derivatives of displacement wrt. reference coordinates
    dudx = np.transpose(displ,(0,1,3,2)) @ dndx

    # Deformation gradient
    dfgrd = np.identity(dof) + dudx

    return dfgrd