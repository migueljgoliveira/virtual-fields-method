from numpy import diff
from scipy.optimize import least_squares, differential_evolution

import _funcs

def identication_aux(x0,strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,
                     ntens,nstatev,nvfs,nf,props,opti,constr,nprops,nlgeom):

    # Update material properties
    props[opti] = x0

    # Apply user-defined properties constraints
    props = _funcs.properties_constraints(props,constr)

    # Core of virtual fields method
    ivw,evw,res,phi = _funcs.vfm_core(strain,rot,dfgrd,rotm,force,vol,vfs,
                                      props,nprops,ne,dof,ndi,nshr,ntens,
                                      nstatev,nvfs,nf,nlgeom)

    print(x0,phi)

    return res  

def identification(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,
                   nstatev,nvfs,nf,props,opti,bounds,constr,nprops,nlgeom):

    result = least_squares(identication_aux,
                           args = (strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,
                                   ndi,nshr,ntens,nstatev,nvfs,nf,props,opti,
                                   constr,nprops,nlgeom),
                           x0 = props[opti],
                           method = 'lm',
                           ftol = 1e-8, xtol = 1e-8, gtol = 1e-8,
                           x_scale = 'jac',
                           max_nfev = 1000,
                           diff_step = 1e-8,
                          )

    return