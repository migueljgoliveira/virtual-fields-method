import numpy as np

import _funcs

def strain_displacement(coord,conn,bcfix,nn,ne,npe,dof,ncomp,nlgeom):
    """
    Compute the elements strain-displacement matrix.

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    conn : (ne,npe) , int
        Elements connectivity.
    bcfix : (nbcfix) , int
        Fixed degrees of freedom.
    ne : int
        Number of elements.
    npe : int
        Number of nodes per element.
    dof : int
        Number of degrees of freedom.
    ntens : int
        Number of tensor components.
    ncomp : int
        Number of tensor components depending on deformation formulation.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).

    Returns
    -------
    bg : (ne*ncomp,nn*dof) , float
        Global strain-displacement matrix.
    mbginv : (ne*ncomp,nn*dof) , float
        Pseudo-inverse of modified global strain-displacement matrix.
    ielems : , int
        Index of elements components in global strain-displacement matrix.

    Notes
    -----
    nbcfix : int
        Number of fixed degrees of freedom.
    """

    # Partial derivatives of shape functions and jacobian
    if npe == 4:
        dNdnr,jac,_ = _funcs.el_quad4r(coord[conn],0)
    elif npe == 8:
        dNdnr,jac,_ = _funcs.el_hex8r(coord[conn])

    # Partial derivatives of shape functions wrt to cartesian coordinates
    dNdx = np.linalg.inv(jac) @ dNdnr

    # Initialise element strain-displacement matrix
    be = np.zeros((ne,ncomp,npe*dof))

    # Indices for matrix allocation
    idx = np.arange(0,npe*dof,dof)

    # Compute elements strain-displacement matrix
    if npe == 4:

        be[:,0,idx  ] = dNdx[:,0,:]
        be[:,1,idx+1] = dNdx[:,1,:]

        if nlgeom:
            be[:,2,idx  ] = dNdx[:,1,:]
            be[:,3,idx+1] = dNdx[:,0,:]
        else:
            be[:,2,idx  ] = dNdx[:,1,:]
            be[:,2,idx+1] = dNdx[:,0,:]

    elif npe == 8:

        be[:,0,idx  ] = dNdx[:,0,:]
        be[:,1,idx+1] = dNdx[:,1,:]
        be[:,2,idx+2] = dNdx[:,2,:]

        if nlgeom:
            be[:,3,idx  ] = dNdx[:,1,:]
            be[:,4,idx+1] = dNdx[:,0,:]

            be[:,5,idx  ] = dNdx[:,2,:]
            be[:,6,idx+2] = dNdx[:,0,:]

            be[:,7,idx+1] = dNdx[:,2,:]
            be[:,8,idx+2] = dNdx[:,1,:]
        else:
            be[:,3,idx  ] = dNdx[:,1,:]
            be[:,3,idx+1] = dNdx[:,0,:]

            be[:,4,idx  ] = dNdx[:,2,:]
            be[:,4,idx+2] = dNdx[:,0,:]

            be[:,5,idx+1] = dNdx[:,2,:]
            be[:,5,idx+2] = dNdx[:,1,:]

    # Assembly global strain-displacement matrix
    bg = np.zeros((ne*ncomp,nn*dof))
    ielems = np.zeros((ne,ncomp),dtype=int)
    for i in range(ne):

        # Columns dof index 
        idofs = np.vstack((conn[i]*dof,conn[i]*dof+1)).T.flatten()

        # Rows element index
        ielems[i] = np.array([j*ne+i for j in range(ncomp)])

        # Assign element matrix to global matrix
        bg[ielems[i][:,None],idofs] = be[i]

    # Apply fixed boundary conditions to global strain-displacement matrix
    mbg = np.delete(bg,bcfix,1)

    # Compute the pseudo-inverse of modified global strain-displacement matrix
    mbginv = np.linalg.pinv(mbg)

    return bg,mbginv,ielems