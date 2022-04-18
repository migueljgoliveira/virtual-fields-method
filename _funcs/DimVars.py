import numpy as np

def dim_vars(coord,conn,nt,nlgeom):
    """
    Set dimensional variables.

    Parameters
    ----------
    coord : (nt,(nn,dof)) , float
        Nodes reference coordinates.
    conn : (nt,(ne,npe)) , int
        Elements connectivity.
    nt : int
        Number of tests.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).

    Returns
    -------
    nn : (nt,) , int
        Number of nodes.
    ne : (nt,) , int
        Number of elements.
    npe : (nt,) , int
        Number of nodes per element.
    dof : (nt,) , int
        Number of degrees of freedom.
    ndi : (nt,) , int
        Number of normal tensor components.
    nshr : (nt,) , int
        Number of shear tensor components.
    ntens : (nt,) , int
        Number of tensor components.
    ncomp : (nt,) , int
        Number of tensor components depending on deformation formulation.
    nstatev : (nt,) , int
        Number of internal state variables.
    """

    # Initialize dim variables
    nn = np.zeros(nt,dtype=int)
    ne = np.zeros(nt,dtype=int)
    npe = np.zeros(nt,dtype=int)
    dof = np.zeros(nt,dtype=int)
    ndi = np.zeros(nt,dtype=int)
    nshr = np.zeros(nt,dtype=int)
    ntens = np.zeros(nt,dtype=int)
    ncomp = np.zeros(nt,dtype=int)
    nstatev = np.zeros(nt,dtype=int)

    for t in range(nt):

        # Number of nodes 
        nn[t] = coord[t].shape[0]

        # Number of elements
        ne[t] = conn[t].shape[0]

        # Number of nodes per element
        npe[t] = conn[t].shape[1]

        # Degrees of freedom
        dof[t] = coord[t].shape[1]

        # Number of normal and shear components
        if dof[t] == 2:
            ndi[t] = 2
            nshr[t] = 1
        elif dof[t] == 3:
            ndi[t] = 3
            nshr[t] = 3

        # Number of tensor components
        ntens[t] = ndi[t] + nshr[t]

        # Number of tensor components depending on deformation formulation
        if nlgeom:
            ncomp = dof*dof
        else:
            ncomp = ntens

        # Number of internal state variables
        nstatev[t] = ntens[t] + 1

    return nn,ne,npe,dof,ndi,nshr,ntens,ncomp,nstatev