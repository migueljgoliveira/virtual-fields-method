import numpy as np

def scaling_virtual_fields(ivw,scale,nf):
    """
    Compute scaling parameter for sensitivity-based virtual fields.

    Parameters
    ----------
    ivw : (nvfs,nf) , float
        Internal virtual work.
    scale : float
        Scaling 
    nf : int
        Number of increments.

    Returns
    -------
    alpha : (nvfs,1) , float
        Scaling parameter.
    """

    # Sort internal virtual work absolute values in descening order
    sortivw = np.sort(abs(ivw))[:,::-1]

    # Compute number ot time increments to consider
    nsteps = int(np.floor(nf*scale))
    if nsteps == 0: nsteps = 1

    # Compute mean of internal virtual work
    meanivw = np.mean(sortivw[:,:nsteps],1)
    meanivw[meanivw == 0] = 1

    # Compute scaling parameter
    alpha = (1/meanivw)[:,None]

    return alpha