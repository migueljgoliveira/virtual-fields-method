import numpy as np

import _funcs
from ummdp_vfm import ummdp_vfm as umat

def cauchy_stress(strain,rot,rotm,ne,dof,ndi,nshr,ntens,nstatev,nf,nprops,
                  props,voigt):
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
    voigt : bool
        Flag for voigt notation (0/1).

    Returns
    -------
    stress : (nf,ne,dof,dof) , float
        Cauchy stress in global csys.
    statev : (nf,ne,ntens+1) , float
        Internal state variables in global csys.
    d33 : (nf,ne) , float
        Strain in thickness direction.
    """

    # Stress integration variables
    stress = np.zeros((nf,ne,ntens))
    dstrain = np.zeros((nf,ne,ntens))
    statev = np.zeros((nf,ne,nstatev))
    d33 = np.zeros((nf,ne))

    try:
        # Loop over time increments
        for i in range(1,nf):
            kinc = i
            # Loop over elements
            for j in range(ne):
                noel = j + 1

                # Total strain increment
                dstrain[i,j,:] = strain[i,j,:]  - strain[i-1,j,:]

                # Stress integration in corotational material csys
                stress[i,j,:],statev[i,j,:],d33[i,j],er = umat(stress[i-1,j,:],
                                                               statev[i-1,j,:],
                                                               strain[i,j,:],
                                                               dstrain[i,j,:],
                                                               ndi,nshr,ntens,
                                                               nstatev,
                                                               props,nprops,
                                                               noel,1,kinc)

                # Check if ummdp returns any error
                if er != 0:
                    raise StopIteration
    except StopIteration as e:
        print('Error >> stress calculation failed, check ummdp log file.')
        return

    # Compute thickness strain for plane stress problems
    if dof == 2:
        d33 = _funcs.strain33(strain,statev[i,j,1:],props[3])

    # Rotate cauchy stress to global csys and convert to tensor form
    stress = _funcs.rotate_tensor(stress,rot,rotm,ne,dof,ndi,nshr,ntens,nf,
                                  dir=1,voigt=voigt)

    # Rotate statev to global csys
    statev[...,1:] = _funcs.rotate_tensor(statev[...,1:],rot,rotm,ne,dof,ndi,
                                          nshr,ntens,nf,dir=1,voigt=1,eng=0)

    return stress,statev,d33