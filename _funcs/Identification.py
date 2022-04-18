import numpy as np
from scipy.optimize import least_squares, differential_evolution

import _funcs

def identication_main(x,strain,rot,dfgrd,rotm,force,time,vol,bg,mbginv,bccte,
                      bcact,ielems,vfs,nn,ne,npe,dof,ndi,nshr,ntens,ncomp,
                      nstatev,nvfs,nf,nt,nprops,props,vars,nvars,bounds,constr,
                      nlgeom,symm,ivfs,algo,tests,fout,refvars):
    """
    Perform identification of material properties. 

    Parameters
    ----------
    x : (nvars,) , float
        Updated identification properties.
    strain : (nt, (nf,ne,ntens) ) , float
        Strain in corotational material csys.
    rot : (nt, (nf,ne,dof,dof) ) , float
        Rotation tensor.
    dfgrd : (nt, (nf,ne,dof,dof) ) , float
        Deformation gradient.
    rotm : (nt, (dof,dof) ) , float
        Material rotation tensor.
    force : (nt, (nf,dof) ) , float
        Global loading force.
    time : (nt, (nf,) ) , float
        Time increments.
    vol : (nt,(ne,)) , float
        Elements volume.
    bg : (nt, (ne*ncomp,nn*dof) ) , float
        Global strain-displacement matrix.
    mbginv : (nt, (ne*ncomp,nn*dof) ) , float
        Pseudo-inverse of modified global strain-displacement matrix.
    ielems : (nt, (ne,npe) ) , int
        Index of elements components in global strain-displacement matrix.
    bccte : (nt, (4,()) ) , int
        Contant degrees of freedom per edge.
    bcact : (nt, (nbcact) ) , int
        Active degrees of freedom.
    vfs : (nt, {(nvfs,ne,dof*dof), (nvfs,nn,dof)} ) , float
        Generated virtual fields.
    nn : (nt,) , int
        Number of nodes.
    ne : (nt,) , int
        Number of elements.
    npe : (nt,) , int
        Number of nodes per element.
    dof : (nt,) , int
        Number of degrees of freedom.
    ndi : (nt,) , int
        Number of normal tensor components.
    nshr : (nt,) , int
        Number of shear tensor components.
    ntens : (nt,) , int
        Number of tensor components.
    ncomp : (nt,) , int
        Number of tensor components depending on deformation formulation.
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
    nvars : int
        Number of identification variables.
    bounds : (nvars,2) , float
        Boundaries for identification variables.
    constr : (nprops,2) , float
        Constraints for material properties.
    refvars : (nvars,) , float
        Initial identification variables.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    symm : (nt, (nsymm,) ), int
        List of symmetry conditions.
    ivfs : (nt, {'ud' or 'sb'} ) , int
        List of selected virtual fields.
    algo : str
        Name of optimization algorithm.
    tests : (nt,) , str
        List of tests name.
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
    """

    # Declare variables for best solution
    global it,bestx,bestphi

    # Update iteration number
    it += 1

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
    _,_,res,phi = _funcs.simulation(strain,rot,dfgrd,rotm,force,time,vol,bg,
                                    mbginv,bccte,bcact,ielems,vfs,nn,ne,npe,
                                    dof,ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,
                                    nt,nprops,props,vars,nlgeom,symm,ivfs,
                                    tests,fout)

    # Concatenates total vector of residuals
    resT = np.concatenate(res)

    # Compute total cost function
    phiT = np.sum(phi)

    # Save best solution
    if (bestphi == None) or (phiT < np.sum(bestphi)):
        bestx = x
        bestphi = phi

    # Print variables and total cost function progress to screen and log file
    _funcs.print_progress(it,x,bestx,phi,bestphi,nvars,nt,fout)

    # Write variables and cost function progress to file
    _funcs.write_progress(it,x,phi,nvars,nt,fout)
    _funcs.write_progress(it,bestx,bestphi,nvars,nt,fout,'Best')

    # _funcs.plot_progress(it,bestphi)

    # Return vector of residuals
    if algo in ['lm']:
        return resT

    # Return scalar cost function
    elif algo in ['de']:
        return phiT

def identification(strain,rot,dfgrd,rotm,force,time,vol,bg,mbginv,bccte,bcact,
                   ielems,vfs,nn,ne,npe,dof,ndi,nshr,ntens,ncomp,nstatev,nvfs,
                   nf,nt,nprops,nvars,props,vars,bounds,constr,nlgeom,symm,
                   ivfs,algo,tests,fout):
    """
    Perform identification of material properties. 

    Parameters
    ----------
    strain : (nt, (nf,ne,ntens) ) , float
        Strain in corotational material csys.
    rot : (nt, (nf,ne,dof,dof) ) , float
        Rotation tensor.
    dfgrd : (nt, (nf,ne,dof,dof) ) , float
        Deformation gradient.
    rotm : (nt, (dof,dof) ) , float
        Material rotation tensor.
    force : (nt, (nf,dof) ) , float
        Global loading force.
    time : (nt, (nf,) ) , float
        Time increments.
    vol : (nt,(ne,)) , float
        Elements volume.
    bg : (nt, (ne*ncomp,nn*dof) ) , float
        Global strain-displacement matrix.
    mbginv : (nt, (ne*ncomp,nn*dof) ) , float
        Pseudo-inverse of modified global strain-displacement matrix.
    ielems : (nt, (ne,npe) ) , int
        Index of elements components in global strain-displacement matrix.
    bccte : (nt, (4,()) ) , int
        Contant degrees of freedom per edge.
    bcact : (nt, (nbcact) ) , int
        Active degrees of freedom.
    vfs : (nt, {(nvfs,ne,dof*dof), (nvfs,nn,dof)} ) , float
        Generated virtual fields.
    nn : (nt,) , int
        Number of nodes.
    ne : (nt,) , int
        Number of elements.
    npe : (nt,) , int
        Number of nodes per element.
    dof : (nt,) , int
        Number of degrees of freedom.
    ndi : (nt,) , int
        Number of normal tensor components.
    nshr : (nt,) , int
        Number of shear tensor components.
    ntens : (nt,) , int
        Number of tensor components.
    ncomp : (nt,) , int
        Number of tensor components depending on deformation formulation.
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
    nvars : int
        Number of identification variables.
    bounds : (nvars,2) , float
        Boundaries for identification variables.
    constr : (nprops,2) , float
        Constraints for material properties.
    refvars : (nvars,) , float
        Initial identification variables.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    symm : (nt, (nsymm,) ), int
        List of symmetry conditions.
    ivfs : (nt, {'ud' or 'sb'} ) , int
        List of selected virtual fields.
    algo : str
        Name of optimization algorithm.
    tests : (nt,) , str
        List of tests name.
    fout : str
        Name of output folder.

    Returns
    -------
    props : (nprops,) , float
        Final solution of material properties.
    """

    # Initialize global variables to save best solution
    global it,bestx,bestphi
    it,bestx,bestphi = 0,None,None

    # Set identification variables
    refvars = props[vars]

    # Set boundaries of identification variables
    bounds = bounds[vars]

    # Normalise identification properties
    x = _funcs.normalise_properties(refvars,refvars,bounds,algo,1)

    # Set arguments for identification function
    args = (strain,rot,dfgrd,rotm,force,time,vol,bg,mbginv,bccte,bcact,ielems,
            vfs,nn,ne,npe,dof,ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,nt,nprops,
            props,vars,nvars,bounds,constr,nlgeom,symm,ivfs,algo,tests,fout,
            refvars)

    # Start identification algorithm
    if algo == 'lm':
        result = least_squares(identication_main,
                               args = args,
                               x0 = x,
                               method = 'lm',
                               ftol = 1e-8, xtol = 1e-8, gtol = 1e-8,
                               x_scale = 'jac',
                               max_nfev = int(1e8),
                               diff_step = 1e-8)

    elif algo == 'de':
        result = differential_evolution(identication_main,
                                        args = args,
                                        bounds =  np.tile([0,1],(nvars,1)),
                                        tol = 1e-8, atol = 1e-8,
                                        init = 'latinhypercube',
                                        maxiter = int(1e8))

    # Get identification results
    nit = it
    tmsg = result.message

    # Update material properties with best identification variables
    props[vars] = bestx

    # Run one simulation with best identification variables
    _funcs.simulation(strain,rot,dfgrd,rotm,force,time,vol,bg,mbginv,bccte,
                      bcact,ielems,vfs,nn,ne,npe,dof,ndi,nshr,ntens,ncomp,
                      nstatev,nvfs,nf,nt,nprops,props,vars,nlgeom,symm,ivfs,
                      tests,fout)

    # Print summary of identification results to log
    _funcs.print_result(nit,bestx,bestphi,tmsg,nvars,nt,fout)

    return props