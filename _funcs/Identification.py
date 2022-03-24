import numpy as np
from scipy.optimize import least_squares, differential_evolution

import _funcs

def identication_aux(x,strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,
                     ntens,nstatev,nvfs,nf,nt,nprops,props,vars,nvars,bounds,
                     constr,nlgeom,algo,fout,refvars):
    """
    Perform identification of material properties. 

    Parameters
    ----------
    x : (nvars,) , float
        Updated identification properties.
    strain : (nt,(nf,ne,ntens)) , float
        Strain in corotational material csys.
    rot : (nt,(nf,ne,dof,dof)) , float
        Rotation tensor.
    dfgrd : (nt,(nf,ne,dof,dof)) , float
        Deformation gradient.
    rotm : (nt,(dof,dof)) , float
        Material rotation tensor.
    force : (nt,(nf,dof)) , float
        Global loading force.
    vol : (nt,(ne,)) , float
        Elements volume.
    vfs : (nt,{(nvfs,ne,dof,dof), (nvfs,nn,dof)}) , float
        User defined virtual fields.
    ne : (nt,) , int
        Number of elements.
    dof : (nt,) , int
        Number of degrees of freedom.
    ndi : (nt,) , int
        Number of normal tensor components.
    nshr : (nt,) , int
        Number of shear tensor components.
    ntens : (nt,) , int
        Number of tensor components.
    nstatev : (nt,) , int
        Number of internal state variables.
    nvfs : (nt,) , int
        Number of virtual fields.
    nf : (nt,) , int
        Number of increments.
    nt : int
        Number of tests.
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Updated material properties.
    vars : (nprops,) , bool
        Flags for identification variables.
    bounds : (nvars,2) , float
        Boundaries for identification variables.
    constr : (nprops,2) , float
        Constraints for material properties.
    refvars : (nvars,) , float
        Initial identification variables.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    algo : str
        Name of optimization algorithm.
    fout : str
        Name of output folder.
    bestx : None or (nvars,) , float
        Current best identification variables.
    bestphi : None or float
        Current best cost function.

    Returns
    -------
    props : (nprops,) , float
        Final solution of material properties.

    Notes
    -----
    nvars : int
        Number of identification variables.
    """

    # Declare variables for best solution
    global bestx,bestphi

    # Transform identification variables to apply boundaries
    if (algo in ['lm']) and (not np.isnan(bounds).any()):
        x = _funcs.transform_properties(x,refvars,bounds)

    # De-normalise identification variables and update material properties
    x = _funcs.normalise_properties(x,refvars,bounds,algo,-1)

    # Update material properties with current solution
    props[vars] = x

    # Apply user-defined properties constraints
    if len(constr) > 0:
        props = _funcs.properties_constraints(props,constr)

    # Perform vfm simulation with current solution
    res,phi = _funcs.simulation(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,
                                nshr,ntens,nstatev,nvfs,nf,nt,nprops,props,
                                nlgeom)

    # Concatenates total vector of residuals
    resT = np.concatenate(res)

    # Compute total cost function
    phiT = np.sum(phi)

    # Save best solution
    if (bestphi == None) or (phiT < np.sum(bestphi)):
        bestx = x
        bestphi = phi

    # Write variables and cost function progress to file
    _funcs.write_progress(x,phi,nvars,nt,fout)
    _funcs.write_progress(bestx,bestphi,nvars,nt,fout,'Best')

    # Return vector of residuals
    if algo in ['lm']:
        return resT

    # Return scalar cost function
    elif algo in ['de']:
        return phiT

def identification(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,
                   nstatev,nvfs,nf,nt,nprops,nvars,props,vars,bounds,constr,
                   nlgeom,algo,fout):
    """
    Perform identification of material properties. 

    Parameters
    ----------
    strain : (nt,(nf,ne,ntens)) , float
        Strain in corotational material csys.
    rot : (nt,(nf,ne,dof,dof)) , float
        Rotation tensor.
    dfgrd : (nt,(nf,ne,dof,dof)) , float
        Deformation gradient.
    rotm : (nt,(dof,dof)) , float
        Material rotation tensor.
    force : (nt,(nf,dof)) , float
        Global loading force.
    vol : (nt,(ne,)) , float
        Elements volume.
    vfs : (nt,{(nvfs,ne,dof,dof), (nvfs,nn,dof)}) , float
        User defined virtual fields.
    ne : (nt,) , int
        Number of elements.
    dof : (nt,) , int
        Number of degrees of freedom.
    ndi : (nt,) , int
        Number of normal tensor components.
    nshr : (nt,) , int
        Number of shear tensor components.
    ntens : (nt,) , int
        Number of tensor components.
    nstatev : (nt,) , int
        Number of internal state variables.
    nvfs : (nt,) , int
        Number of virtual fields.
    nf : (nt,) , int
        Number of increments.
    nt : int
        Number of tests.
    nprops : int
        Number of material properties.
    nvars : int
        Number of identification variables.
    props : (nprops,) , float
        List of material properties.
    vars : (nprops,) , bool
        Flags for identification variables.
    bounds : (nvars,2) , float
        Boundaries for identification variables.
    constr : (nprops,2) , float
        Constraints for material properties.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    algo : str
        Name of optimization algorithm.
    fout : str
            Name of output folder.

    Returns
    -------
    props : (nprops,) , float
        Final solution of material properties.
    """

    # Initialize variables for best solution
    global bestx,bestphi
    bestx,bestphi = None,None

    # Set identification variables
    refvars = props[vars]

    # Set boundaries of identification variables
    bounds = bounds[vars]

    # Normalise identification properties
    x = _funcs.normalise_properties(refvars,refvars,bounds,algo,1)

    # Set arguments for identification function
    args = (strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,nstatev,
            nvfs,nf,nt,nprops,props,vars,nvars,bounds,constr,nlgeom,algo,fout,
            refvars)

    # Select optimization algorithm
    # Levenberg-Marquardt
    if algo == 'lm':
        result = least_squares(identication_aux,
                               args = args,
                               x0 = x,
                               method = 'lm',
                               ftol = 1e-8, xtol = 1e-8, gtol = 1e-8,
                               x_scale = 'jac',
                               max_nfev = 1000,
                               diff_step = 1e-8,
                              )

    # Differential Evolution
    elif algo == 'de':
        result = differential_evolution(identication_aux,
                                        args = args,
                                        bounds =  np.tile([0,1],(nvars,1)),
                                        tol = 1e-8, atol = 1e-8,
                                        init = 'latinhypercube',
                                        maxiter = 10000,
                                        )

    # Get best identification variables
    xf = result.x

    # Transform best identification variables to apply boundaries
    if (algo in ['lm']) and (not np.isnan(bounds).any()):
        xf = _funcs.transform_properties(xf,refvars,bounds)

    # De-normalise best identification variables
    xf = _funcs.normalise_properties(xf,refvars,bounds,algo,-1)

    # Update material properties with best identification variables
    props[vars] = xf

    # Run one simulation with best identification variables
    res,phi = _funcs.simulation(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,
                                ndi,nshr,ntens,nstatev,nvfs,nf,nt,nprops,
                                props,nlgeom)

    return props