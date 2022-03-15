import numpy as np
from scipy.optimize import least_squares, differential_evolution

import _funcs

def identication_aux(x,strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,
                     nshr,ntens,nstatev,nvfs,nf,nt,refprops,bounds,nlgeom,algo,
                     props,nprops,opti,constr):
    """
    Perform identification of material properties. 

    Parameters
    ----------
    x : (nid,) , float
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
    refprops : (nid,) , float
        Initial identification properties.
    bounds : (nid,2) , float
        Boundaries for identification properties.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    algo : str
        Name of optimization algorithm.
    props : (nprops,) , float
        Updated material properties.
    nprops : int
        Number of material properties.
    opti : (nprops,) , bool
        Flags for identification properties.
    constr : (nprops,2) , float
        Constraints for identification properties.

    Returns
    -------
    props : (nprops,) , float
        Final solution of material properties.

    Notes
    -----
    nid : int
        Number of identification properties.
    """

    # De-normalise identification properties and update material properties
    props[opti] = _funcs.transform_properties(x,refprops,bounds,algo,-1)

    # Apply user-defined properties constraints
    if len(constr) > 0:
        props = _funcs.properties_constraints(props,constr)

    # Virtual fields method core function
    ivw,evw,res,phi = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    for t in range(nt):
        ivw[t],evw[t],res[t],phi[t] = _funcs.vfm_core(strain[t],rot[t],
                                                      dfgrd[t],rotm[t],
                                                      force[t],vol[t],vfs[t],
                                                      ne[t],dof[t],ndi[t],
                                                      nshr[t],ntens[t],
                                                      nstatev[t],nvfs[t],nf[t],
                                                      nlgeom,props,nprops)


    # Compute total residuals
    resT = np.concatenate(res)

    # Compute total cost function
    phiT = np.sum(phi)/nt

    print(x,props[opti],phiT)

    # Return residuals or scalar depending of algorithm
    if algo in ['lm']:
        return resT
    elif algo in ['de']:
        return phiT

    # result.cost = 0.5*np.sum(result.fun**2)
    # result.fun --> res

def identification(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,
                   nstatev,nvfs,nf,nt,options):
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
    options : object
        Object with project options.

    Returns
    -------
    props : (nprops,) , float
        Final solution of material properties.
    """

    # Copy identification properties
    refprops = np.copy(options.props[options.opti])

    # Copy boundaries of identification properties
    try:
        bounds = options.bounds[options.opti]
    except:
        bounds = []

    # Normalise identification properties
    x,idbounds = _funcs.transform_properties(refprops,refprops,bounds,
                                             options.algo,1)

    # Arguments for identification function
    args = (strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,nstatev,
            nvfs,nf,nt,refprops,bounds,options.nlgeom,options.algo,
            options.props,options.nprops,options.opti,options.constr)

    # Levenberg-Marquardt
    if options.algo == 'lm':
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
    elif options.algo == 'de':
        result = differential_evolution(identication_aux,
                                        args = args,
                                        bounds = idbounds,
                                        tol = 1e-8, atol = 1e-8,
                                        init = 'latinhypercube',
                                        maxiter = 10000,
                                        )

    # De-normalise identification properties
    x = _funcs.transform_properties(result.x,refprops,bounds,options.algo,-1)

    # Update material properties with best solution
    options.props[options.opti] = x

    return options.props