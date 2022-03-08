import numpy as np

def VoigtToTensor(voigt,ne,dof,ndi,nshr,ntens,nf,eng=0):
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
    ndi : int
        Number of normal tensor components.
    nshr : int
        Number of shear tensor components.
    ntens : int
        Number of tensor components.
    nf : int 
        Number of increments.
    eng : bool
        Flag for engineering strain (0/1).

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
        for i in range(ndi):
            for j in range(ndi):
                if i != j:
                    n = (i+j)+(2-ndi+nshr)
                    tensor[...,i,j] = voigt[...,n]/2


    return tensor
