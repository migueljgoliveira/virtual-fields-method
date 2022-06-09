import numpy as np

import _funcs
import _utils

def cauchy_stress(strain,rot,rotm,ne,dof,ndi,nshr,ntens,nstatev,nf,nprops,
                  props,fout,voigt=False):
    """
    Compute the cauchy stress in local csys using the backward-Euler with an elastic predictor and plastic corrector.

    Parameters
    ----------
    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    rotm : (dof,dof) , float
        Material rotation tensor.
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
    nstatev : int
        Number of internal state variables.
    nf : int
        Number of increments.
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Material properties.
    fout : str
        Name of output folder.
    voigt : bool
        Flag for voigt notation (False/True).

    Returns
    -------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.
    statev : (nf,ne,ntens+1) , float
        Internal state variables in local csys.
    de33 : (nf,ne) , float
        Strain in thickness direction (plane stress).
    success : bool
        Variable to monitor the sucess of stress reconstruction (False/True).
    """

    # Initialize f2py external stop function
    _funcs.ummdp_vfm.f2py_stop = _utils.f2py_stop

    # Stress integration in corotational material csys
    try:
        stress,statev,de33 = _funcs.ummdp_vfm.ummdp_vfm(strain,ne,ndi,nshr,
                                                        ntens,nstatev,props,
                                                        nprops,nf,fout)

        success = True

    except Exception:
        stress = np.zeros((nf,ne,ntens))
        statev = np.zeros((nf,ne,ntens+1))
        de33 = np.zeros((nf,ne))

        success = False

    # Rotate cauchy stress to global csys and convert to tensor form
    stress = _utils.rotate_tensor(stress,rot,rotm,ne,dof,ndi,ntens,nf,
                                  dir=1,voigt=voigt)

    return stress,statev,de33,success