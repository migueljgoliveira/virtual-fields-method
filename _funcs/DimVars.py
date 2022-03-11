def dim_vars(coord,conn,lvfs):
    """
    Set dimensional variables.

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    conn : (ne,npe) , int
        Elements connectivity.
    lvfs : (nvfs,) , int
        List of user defined virtual fields type. 

    Returns
    -------
    nn : int
        Number of nodes.
    ne : int
        Number of elements.
    npe : int
        Number of nodes per element.
    dof : int
        Number of degrees of freedom.
    ndi : int
        Number of normal tensor components.
    nshr : int
        Number of shear tensor components.
    ntens : int
        Number of tensor components.
    nstatev : int
        Number of internal state variables.
    nvfs : int
        Number of virtual fields.
    """

    # Number of nodes 
    nn = coord.shape[0]

    # Number of elements
    ne = conn.shape[0]

    # Number of nodes per element
    npe = conn.shape[1]

    # Degrees of freedom
    dof = coord.shape[1]

    # Number of normal and shear components
    if dof == 2:
        ndi = 2
        nshr = 1
    elif dof == 3:
        ndi = 3
        nshr = 3

    # Number of tensor components
    ntens = ndi + nshr

    # Number of internal state variables
    nstatev = ntens + 1

    # Number of user defined virtual fields
    nvfs = len(lvfs)

    return nn,ne,npe,dof,ndi,nshr,ntens,nstatev,nvfs