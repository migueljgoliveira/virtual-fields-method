import numpy as np

def TensorToVoigt(tensor,ne,ndi,ntens,nf,eng=0):
    """ 
    Convert tensor to voigt form.

    Parameters
    ----------
    tensor : (nf,ne,dof,dof),float
        Array in tensor form.
    ne : int
        Number of elements.
    ndi : int
        Number of normal tensor components.
    ntens : int
        Number of tensor components.
    nf : int 
        Number of increments.
    eng : bool
        Flag for engineering strain (0/1).

    Returns
    -------
    voigt : (nf,ne,ntens),float
        Array in voigt notation.

    Notes
    -----
    dof : int
        Number of degrees of freedom.
    """

    voigt = np.zeros((nf,ne,ntens))

    voigt[...,0] = tensor[...,0,0]
    voigt[...,1] = tensor[...,1,1]

    if ntens == 3:
        voigt[...,2] = tensor[...,0,1]
    elif ntens == 6:
        voigt[...,2] = tensor[...,2,2]
        voigt[...,3] = tensor[...,0,1]
        voigt[...,4] = tensor[...,0,2]
        voigt[...,5] = tensor[...,1,2]

    # Engineering strain
    if eng:
        voigt[...,ndi:ntens] = voigt[...,ndi:ntens]*2

    return voigt