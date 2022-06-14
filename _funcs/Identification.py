import warnings
import numpy as np
from functools import partial
from scipy.optimize import minimize

import _funcs

warnings.filterwarnings('ignore')

def fcn_callback(x,strain,rot,dfgrd,rotm,time,bg,mbginv,bcdofs,vfs,nn,ne,dof,
                 ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,nt,nprops,props,vars,
                 nvars,constr,nlgeom,test,fout,dirout):

    # Declare global variables
    global it,fevit,bestphi,ivw,evw

    # Update material properties with current solution
    props[vars] = x

    # Apply user-defined properties constraints
    props = _funcs.properties_constraints(props,constr)

    # Update sensivity-based virtual fields
    for t in range(nt):
        if 'sb' in list(vfs[t].keys()):
            vfs[t] = _funcs.sensivity_based_virtual_fields(strain[t],rot[t],
                                                           dfgrd[t],rotm[t],
                                                           time[t],bg[t],
                                                           mbginv[t],bcdofs[t],
                                                           vfs[t],nn[t],ne[t],
                                                           dof[t],ndi[t],
                                                           nshr[t],ntens[t],
                                                           ncomp[t],nstatev[t],
                                                           nvfs[t],nf[t],
                                                           nprops,props,vars,
                                                           nlgeom,fout)

    # Write virtual work of current solution
    for t in range(nt):
        _funcs.write_virtual_work(ivw[t],evw[t],test[t],nvfs[t],nf[t],nt,
                                  fout,dirout)

    # Print variables and total cost function progress to screen and log file
    _funcs.print_progress(it,fevit,x,bestphi,nvars,nt,fout,dirout,'it')

    # Write variables and cost function progress to file
    _funcs.write_progress(it,fevit,x,bestphi,nvars,nt,fout,dirout)

    # Update iteration number
    it += 1

    # Reset function evaluations per iteration counter
    fevit = 0

    return

def fcn(x,strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,nstatev,
        nvfs,nf,nt,nprops,props,vars,nvars,constr,nlgeom,fout,dirout):

    # Declare global variables
    global fev,fevit,it,fevphi,bestphi,ivw,evw

    # Print iteration header to log file
    if fevit == 0 or ((fevit == 1) and (it == 1)):
        _funcs.print_iteration(it,fout,dirout)

    # Update number of total evaluations
    fev += 1

    # Update current number of evaluations in iteration
    fevit += 1

    # Update material properties with current solution
    props[vars] = x

    # Apply user-defined properties constraints
    props = _funcs.properties_constraints(props,constr)

    # Check validity of current solution
    valid = ~np.isnan(props[vars]).any()

    # Perform vfm simulation with current solution
    if valid:
        ivw,evw,fevphi,success = _funcs.simulation(strain,rot,dfgrd,rotm,force,
                                                   vol,vfs,ne,dof,ndi,nshr,
                                                   ntens,nstatev,nvfs,nf,nt,
                                                   nprops,props,nlgeom,fout)

    # If solution is not valid or stress reconstruction fails return nan
    if (not valid) or (not success):
        fevphi = np.nan

    # # Update cost function with correction factor
    # if 'sb' in list(vfs[t].keys()):
    #     phi,cf = _funcs.correction_factor(res,allphi[-2],cf,it)

    # Compute total cost function
    phi = np.sum(fevphi)

    # Save best cost function
    if (bestphi == None) or (phi < np.sum(bestphi)):
        bestphi = fevphi

    # Print variables and cost function progress to screen and log file
    _funcs.print_progress(it,fevit,x,fevphi,nvars,nt,fout,dirout,'fe')

    # Write variables and cost function progress to file
    _funcs.write_progress(it,fevit,x,fevphi,nvars,nt,fout,dirout)

    # Update number of iteration after initial evaluation
    if it == 0: it += 1

    return phi

def identification(strain,rot,dfgrd,rotm,force,time,vol,bg,mbginv,bcdofs,vfs,
                   nn,ne,dof,ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,nt,nprops,
                   nvars,props,vars,bounds,constr,nlgeom,test,fout,dirout,st):
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
    bcdofs : {'fixed','active','parent','child'} , int
        Boundary conditions degrees of freedom.
    vfs : (nt, {(nvfs,ne,dof*dof), (nvfs,nn,dof)} ) , float
        Settings and generated virtual fields.
    nn : (nt) , int
        Number of nodes.
    ne : (nt) , int
        Number of elements.
    dof : (nt) , int
        Number of degrees of freedom.
    ndi : (nt) , int
        Number of normal tensor components.
    nshr : (nt) , int
        Number of shear tensor components.
    ntens : (nt) , int
        Number of tensor components.
    ncomp : (nt) , int
        Number of tensor components depending on deformation formulation.
    nstatev : (nt) , int
        Number of internal state variables.
    nvfs : (nt) , int
        Number of virtual fields.
    nf : (nt) , int
        Number of increments.
    nt : int
        Number of tests.
    nprops : int
        Number of material properties.
    props : (nprops) , float
        Updated material properties.
    vars : (nprops) , bool
        Flags for identification variables.
    nvars : int
        Number of identification variables.
    bounds : (nvars,2) , float
        Boundaries for identification variables.
    constr : (nprops,2) , float
        Constraints for material properties.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    test : (nt) , str
        List of tests name.
    fout : str
        Name of output folder.
    dirout : str
        Directory of project to export output files.
    st : float
        Start time in seconds since epoch.

    Returns
    -------
    props : (nprops,) , float
        Final solution of material properties.
    """

    # Declare global variables
    global fev,fevit,it,fevphi,bestphi

    # Initialize global variables
    fev,it,fevit = 0,0,0
    fevphi,bestphi = None,None

    # Set arguments for identification function
    args = (strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,nstatev,
            nvfs,nf,nt,nprops,props,vars,nvars,constr,nlgeom,fout,dirout)

    # Generate wrapper for callback function
    fcncb = partial(fcn_callback,strain=strain,rot=rot,dfgrd=dfgrd,rotm=rotm,
                                 time=time,bg=bg,mbginv=mbginv,bcdofs=bcdofs,
                                 vfs=vfs,nn=nn,ne=ne,dof=dof,ndi=ndi,nshr=nshr,
                                 ntens=ntens,ncomp=ncomp,nstatev=nstatev,
                                 nvfs=nvfs,nf=nf,nt=nt,nprops=nprops,
                                 props=props,vars=vars,nvars=nvars,
                                 constr=constr,nlgeom=nlgeom,test=test,
                                 fout=fout,dirout=dirout)

    # Start identification algorithm
    result = minimize(fcn,
                      args = args,
                      x0 = props[vars],
                      method = 'Nelder-Mead',
                      bounds =  bounds[vars],
                      tol = 1e-8,
                      options = {
                                 'maxiter': int(1e8),
                                 'fatol': 1e-8,
                                 'xatol': 1e-8,
                                 'adaptive': True,
                                },
                      callback = fcncb,
                      )

    # Get identification results
    x = result.x
    nit = result.nit
    nfev = result.nfev
    tmsg = result.message

    # Update material properties with best identification variables
    props[vars] = x

    # Print summary of identification results to log
    _funcs.print_result_identification(nit,nfev,x,bestphi,tmsg,nvars,nt,
                                       fout,dirout,st)

    return props