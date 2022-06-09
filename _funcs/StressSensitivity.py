import numpy as np

import _funcs

def stress_sensitivity(strain,rot,dfgrd,rotm,time,dx,ne,dof,ndi,nshr,ntens,
                       ncomp,nstatev,nf,nprops,props,vars,nvfs,nlgeom,fout,
                       flat=1):
    """
    Compute total and incremental stress sensitivity for sensivity-based virtual fields.

    Parameters
    ----------
    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    rotm : (dof,dof) , float
        Material rotation tensor.
    time : (nf,) , float
        Time increments.
    dx : float
        Identification variables perturbation.
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
    ncomp : int
        Number of tensor components depending on deformation formulation.
    nstatev : int
        Number of internal state variables.
    nf : int
        Number of increments.
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Material properties.
    vars : (nprops,) , bool
        Flags for identification variables.
    nvfs : int
        Number of virtual fields.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    fout : str
        Name of output folder.
    flat : bool
        Flag to flatten stress sensitivities by elements and components (0/1).

    Returns
    -------
    ss : (nvfs,nf,ne*ncomp) or (nvfs,nf,ne,dof,dof) , float
        Total stress sensitivity.
    iss : (nvfs,nf,ne*ncomp) or (nvfs,nf,ne,dof,dof) , float
        Incremental stress sensitivity.
    """

    # Set form of cauchy stress depending on deformation framework
    if nlgeom:
        voigt = 0
    else:
        voigt = 1

    # Compute reference cauchy stress on global csys
    stressref,_,de33 = _funcs.cauchy_stress(strain,rot,rotm,ne,dof,ndi,nshr,
                                            ntens,nstatev,nf,nprops,props,fout,
                                            voigt=voigt)

    # Compute reference 1st piola-kirchhoff stress
    if nlgeom:
        pkstressref = _funcs.piola_kirchhoff_stress(stressref,de33,dfgrd,ne,
                                                    dof,nf,flat)

    # Compute time increment
    if flat:
        dtime = (time[1:] - time[:-1])[:,None,None]
    else:
        dtime = (time[1:] - time[:-1])[:,None,None,None]

    # Initialize stress sensitivities
    if flat:
        ss = np.zeros((nvfs,nf,ne,ncomp))
        iss = np.zeros((nvfs,nf,ne,ncomp))
    else:
        ss = np.zeros((nvfs,nf,ne,dof,dof))
        iss = np.zeros((nvfs,nf,ne,dof,dof))

    # Loop over identification variables
    for i in range(nvfs):

        # Copy reference material properties
        dprops = np.copy(props)

        # Add perturbation to identification variable
        dprops[np.flatnonzero(vars)[i]] = props[vars][i] - dx*props[vars][i]

        # Compute cauchy stress on global csys
        stress,_,de33 = _funcs.cauchy_stress(strain,rot,rotm,ne,dof,ndi,nshr,
                                             ntens,nstatev,nf,nprops,dprops,
                                             fout,voigt=voigt)

        # Compute 1st piola-kirchhoff stress
        if nlgeom:
            pkstress = _funcs.piola_kirchhoff_stress(stress,de33,dfgrd,ne,
                                                     dof,nf,flat)

        # Compute total stress sensitivity
        if nlgeom:
            ss[i] = pkstressref - pkstress
        else:
            ss[i] = stressref - stress

        # Compute incremental stress sensitivity
        iss[i,1:] = (ss[i,1:] - ss[i,:-1]) / dtime

    # Flatten stress sensitivities by elements and components
    if flat:
        ss = np.reshape(np.moveaxis(ss,-1,-2),(nvfs,nf,ne*ncomp))
        iss = np.reshape(np.moveaxis(iss,-1,-2),(nvfs,nf,ne*ncomp))

    return ss,iss