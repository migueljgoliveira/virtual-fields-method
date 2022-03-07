def ExternalVirtualWork(force):
    """
    Compute the external virtual work.

    Parameters
    ----------
    force : (nf,dof),float
        Global external force.

    Returns
    -------
    evw : (nf,),float
        External virtual work.

    Notes
    -----
    nf : int
        Number of increments.
    """

    # return evw