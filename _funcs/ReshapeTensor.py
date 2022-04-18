import numpy as np

def reshape_tensor(tensor,ne,dof,nf,dir,nvfs=None):
    """ 
    Flatten tensor and rearrange components order.

    Parameters
    ----------
    tensor : (nf,ne,dof,dof) or (nf,ne,dof*dof), float
        Tensor.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nf : int
        Number of increments.
    nvfs : int
        Number of virtual fields.
    dir : int
        Flag for reshape direction (-1/1).

    Returns
    -------
    retensor : (nf,ne,dof*dof) or (nf,ne,dof,dof) , float
        Reshaped and rearranged tensor.
    """

    # Rearrange components order
    if dir == 1:
        if dof == 2:
            order = [0,3,1,2]
        elif dof == 3:
            order= [0,4,8,1,3,2,6,5,7]
    elif dir == -1:
        if dof == 2:
            order = [0,2,3,1]
        elif dof == 3:
            order= [0,3,5,4,1,7,6,8,2]

    retensor = tensor[...,order]

    # Reshape tensor to flat
    if dir == 1:
        if nvfs is None:
            retensor = np.reshape(tensor,(nf,ne,dof*dof))
        else:
            retensor = np.reshape(tensor,(nvfs,nf,ne,dof*dof))

    # Reshape flat to tensor
    elif dir == -1:
        if nvfs is None:
            retensor = np.reshape(tensor,(nf,ne,dof,dof))
        else:
            retensor = np.reshape(tensor,(nvfs,nf,ne,dof,dof))

    return retensor