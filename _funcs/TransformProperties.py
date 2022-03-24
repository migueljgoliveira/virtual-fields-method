import numpy as np

def transform_properties(x,refvars,bounds):
    """
    Transform identification variables for levenberg-marquardt algorithm.

    Parameters
    ----------
    x : (nid,) , float
        Updated identification variables.
    refvars : (nid,) , float
        Initial identification variables.
    bounds : (nid,2) , float
        Boundaries for identification variables.

    Returns
    -------
    xt : (nid,) , float
        Transformed identification variables.

    Notes
    -----
    nid : int
        Number of identification variables.
    """

    # Copy identification variables
    xt  = x

    if (len(bounds) > 0):

        # Normalise bounds by initial identification variables
        nbounds = bounds/refvars[:, None]

        # Transform identification variables
        uprops = 1 + (nbounds[:,1]-1) * (1-np.exp((1-x)/(nbounds[:,1]-1)))
        lprops = 1 + (nbounds[:,0]-1) * (1-np.exp((1-x)/(nbounds[:,0]-1)))

        # Replace identification variables without boundaries
        uprops[np.isnan(uprops)] = x[np.isnan(uprops)]
        lprops[np.isnan(lprops)] = x[np.isnan(lprops)]

        # Replace identification variables with boundaries
        xt[x >= 1] = uprops[x >= 1]
        xt[x < 1] = lprops[x < 1]

    return xt

