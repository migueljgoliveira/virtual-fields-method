import numpy as np

import _funcs

def log_strain(coord,displ,conn,rotm,thick,ne,npe,dof,ndi,nshr,ntens,nf):
    """
    Compute the logarithmic strain in local csys by the polar 
      decomposition of the deformation gradient.

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    displ : (nf,nn,dof) , float
        Nodes displacements.
    conn : (ne,npe) , int
        Elements connectivity.
    rotm : (dof,dof) , float
        Material rotation tensor.
    thick : float
        Specimen initial thickness.
    ne : int
        Number of elements.
    npe : int
        Number of nodes per element.
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

    Returns
    -------
    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    vol : (ne,) , float
        Elements volume.
    """

    # Derivatives of shape function and jacobian
    if npe == 4:
        dndnr,jac,vol = _funcs.el_quad4r(coord[conn],thick)
    elif npe == 8:
        dndnr,jac,vol = _funcs.el_hex8r(coord[conn])

    # Deformaton gradient
    dfgrd = _funcs.deformation_gradient(displ[:,conn],dndnr,jac,dof)

    # Polar decomposition of deformation gradient to right stretch tensor
    rot,strch = _funcs.polar_decomposition(dfgrd,side='left')

    # Logarithmic strain in global csys
    eigv,eigpr = np.linalg.eig(strch)
    strain = eigpr * np.log(eigv[...,None,:]) @ np.linalg.inv(eigpr)

    # Rotate strain to corotational material csys and convert to voigt
    strain = _funcs.rotate_tensor(strain,rot,rotm,ne,dof,ndi,nshr,ntens,nf,
                                  dir=-1,voigt=1,eng=1)

    return strain,rot,dfgrd,vol