import numpy as np
from ummdp_vfm import ummdp_vfm as umat

def CauchyStress(strain,props,nprops,ne,ndi,nshr,ntens,nstatev,nf):
    """
    Compute the cauchy stress in local csys by the euler-backward integration scheme.

    Parameters
    ----------
    strain : (nf,ne,ntens),float
        Strain in corotational material csys.
    props : (nprops,),float
        Material properties.
    nprops : int
        Number of material properties.
    ne : int
        Number of elements.
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

    Returns
    -------
    stress : (nf,ne,ntens),float
        Cauchy stress in corotational material csys.
    d33 : (nf,ne),float
        Strain in thickness direction.
    """

    # Stress integration variables
    stress = np.zeros((nf,ne,ntens))
    dstrain = np.zeros((nf,ne,ntens))
    d33 = np.zeros((nf,ne))
    statev = np.zeros((nf,ne,nstatev))

    for i in range(1,nf):
        kinc = i
        for j in range(ne):
            noel = j + 1

            # Strain increment
            dstrain[i,j,:] = strain[i,j,:]  - strain[i-1,j,:]

            # Stress integration in corotational material csys
            stress[i,j,:],statev[i,j,:],d33[i,j],err = umat(stress[i-1,j,:],
                                                            statev[i-1,j,:],
                                                            strain[i,j,:],
                                                            dstrain[i,j,:],
                                                            ndi,nshr,ntens,
                                                            nstatev,
                                                            props,nprops,
                                                            noel,1,kinc)

            # Check if ummdp returns any error
            if err != 0:
                raise StopIteration

    return stress,d33