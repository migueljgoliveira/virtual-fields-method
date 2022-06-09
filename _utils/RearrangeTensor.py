import numpy as np

def rearrange_tensor(tensor,ne,dof,nf,d4=1):
    """
    Export experimental finite element mesh to paraview file.

    Parameters
    ----------
    tensor : (nf,ne,dof,dof) , float
        Input tensor.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    nf : int
        Number of increments.
    d4 : int
        Number of fourth-dimension axis.

    Returns
    -------
    tensor : (nf,ne,dof,dof) , float
        Rearranged tensor.
    """

    # Reshape tensor to flat form
    flat = np.reshape(tensor,(d4,nf,ne,dof*dof))

    # Rearrange components order
    if dof == 2:
        order = [0,3,1,2]
    elif dof == 3:
        order= [0,4,8,1,3,2,6,5,7]

    flat = flat[...,order]

    # Reshape flat to tensor form
    tensor = np.reshape(flat,(d4,nf,ne,dof,dof))

    return tensor