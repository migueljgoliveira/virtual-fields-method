import numpy as np

def flatten_tensor(tensor,ne,dof,nf):
    """ 
    Flatten tensor and rearrange components order.

    Parameters
    ----------
    tensor : (nf,ne,dof,dof), float
        Tensor.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nf : int
        Number of increments.

    Returns
    -------
    flat : (nf,ne,dof*dof) , float
        Flatten and rearranged tensor.
    """

    # Reshape tensor to flat form
    flat = np.reshape(tensor,(nf,ne,dof*dof))

    # Rearrange components order
    if dof == 2:
        order = [0,3,1,2]
    elif dof == 3:
        order= [0,4,8,1,3,2,6,5,7]

    flat = flat[...,order]

    return flat