import numpy as np

def external_virtual_work(force,vfs):
    """
    Compute the external virtual work.

    Parameters
    ----------
    force : (nf,dof) , float
        Global loading force.
    vfs : (nvfs,nf,dof) , float
        User defined virtual fields.

    Returns
    -------
    evw : (nf,nvfs) , float
        External virtual work.

    Notes
    -----
    nf : int
        Number of increments.
    dof : int
        Number of degrees of freedom.
    nvfs : int
        Number of virtual fields.
    """

    # Compute external virtual work
    evw = 2 * force[None] * vfs
    # evw = force[None] * vfs[...,0,:]

    # Sum external virtual work along dof
    evw = np.nansum(evw,2)

    return evw