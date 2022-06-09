import numpy as np

def voigt_to_tensor(voigt,ne,dof,ntens,nf,eng=False):
    """
    Convert voigt to tensor form.

    Parameters
    ----------
    voigt (nf,ne,ntens) , float
        Array in voigt notation.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    ntens : int
        Number of tensor components.
    nf : int 
        Number of increments.
    eng : bool
        Flag for engineering strain (False/True).

    Returns
    -------
    tensor : (nf,ne,dof,dof) , float
        Array in tensor form.
    """

    tensor = np.zeros((nf,ne,dof,dof))

    tensor[...,0,0] = voigt[...,0]
    tensor[...,1,1] = voigt[...,1]

    if ntens == 3:
        tensor[...,0,1] = voigt[...,2]
        tensor[...,1,0] = tensor[...,0,1]
    elif ntens == 6:
        tensor[...,2,2] = voigt[...,2]
        tensor[...,0,1] = voigt[...,3]
        tensor[...,1,0] = tensor[...,0,1]
        tensor[...,0,2] = voigt[...,4]
        tensor[...,2,0] = tensor[...,0,2]
        tensor[...,1,2] = voigt[...,5]
        tensor[...,2,1] = tensor[...,1,2]

    # Engineering strain
    if eng:
        shear = np.logical_not(np.identity(dof,dtype=bool))
        tensor[...,shear] = tensor[...,shear]/2

    return tensor
