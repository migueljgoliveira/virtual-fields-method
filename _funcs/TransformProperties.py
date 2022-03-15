import numpy as np

def transform_properties(x0,refprops,bounds,algo,dir):
    """
    Transform and normalise identification properties.

    Parameters
    ----------
    x : (nid,) , float
        Updated identification properties.
    refprops : (nid,) , float
        Initial identification properties.
    bounds : (nid,2) , float
        Boundaries for identification properties.
    algo : str
        Name of optimization algorithm.
    dir : int
        Flag to normalize or de-normalize identification properties (1/-1)

    Returns
    -------
    x : (nid,) , float
        Transformed identification properties.

    Notes
    -----
    nid : int
        Number of identification properties.
    """

    # Normalise identification properties by initial values
    if algo in ['lm']:

        if dir == 1:
            x = x0 / refprops

            return x,bounds

        elif dir == -1:
            x = x0 * refprops

    # Normalise identification properties by boundaries
    elif algo in ['de']:

        if dir == 1:
            x = (x0 - bounds[:,0]) / (bounds[:,1] - bounds[:,0])
            idbounds = np.zeros_like(bounds)
            idbounds[:,1] = 1

            return x,idbounds

        elif dir == -1:
            x = x0 * (bounds[:,1] - bounds[:,0]) + bounds[:,0]

    # Transform identification properties
    if (algo in ['lm']) and (len(bounds) > 0) and (dir == -1):

        # Normalise bounds by initial properties
        nbounds = bounds/refprops[:, None]

        # Compute transformed properties
        uprops = 1 + (nbounds[:,1]-1) * (1-np.exp((1-x0)/(nbounds[:,1]-1)))
        lprops = 1 + (nbounds[:,0]-1) * (1-np.exp((1-x0)/(nbounds[:,0]-1)))

        # Replace properties without boundares
        uprops[np.isnan(uprops)] = x0[np.isnan(uprops)]
        lprops[np.isnan(lprops)] = x0[np.isnan(lprops)]

        # De-normalised identification properties
        x[x0 >= 1] = (uprops * refprops)[x0 >= 1]
        x[x0 < 1] = (lprops * refprops)[x0 < 1]

    return x

