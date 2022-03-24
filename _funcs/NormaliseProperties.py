def normalise_properties(x,refvars,bounds,algo,dir):
    """
    Transform and normalise identification properties.

    Parameters
    ----------
    x : (nid,) , float
        Updated identification variables.
    refvars : (nid,) , float
        Initial identification variables.
    bounds : (nid,2) , float
        Boundaries for identification variables.
    algo : str
        Name of optimization algorithm.
    dir : int
        Flag to normalize or de-normalize identification variables (1/-1).

    Returns
    -------
    xn : (nid,) , float
        Normalized or de-normalized identification variables.

    Notes
    -----
    nid : int
        Number of identification variables.
    """

    # Normalise identification variables by initial values
    if algo in ['lm']:

        if dir == 1:
            xn = x / refvars

        elif dir == -1:
            xn = x * refvars

    # Normalise identification variables by boundaries
    elif algo in ['de']:

        if dir == 1:
            xn = (x - bounds[:,0]) / (bounds[:,1] - bounds[:,0])

        elif dir == -1:
            xn = x * (bounds[:,1] - bounds[:,0]) + bounds[:,0]

    return xn