import numpy as np
import _subroutines

def LogStrain(coord,displ,rotm,ne,npe,dof,ndi,nshr,ntens,nf):
    """
    Compute the logarithmic strain in local csys by the polar 
      decomposition of the deformation gradient.

    Parameters
    ----------
    coord : (ne,npe,dof),float
        Nodes reference coordinates.
    displ : (nf,ne,npe,dof),float
        Nodes displacements.
    rotm : (dof,dof),float
        Material rotation tensor.
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
    strain : (nf,ne,ntens),float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof),float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof),float
        Deformation gradient.
    """

    # Derivatives of shape function and jacobian
    if npe == 4:
        dNdNr,jac,_ = _subroutines.ElQuad4R(coord)
    elif npe == 8:
        dNdNr,jac,_ = _subroutines.ElHex8R(coord)

    # Deformaton gradient
    dfgrd = _subroutines.DeformationGradient(displ,dNdNr,jac,dof)

    # Polar decomposition of deformation gradient
    rot,strch = _subroutines.PolarDecomposition(dfgrd,side='left')

    # Logarithmic strain in global csys
    eigv,eigpr = np.linalg.eig(strch)
    strain = eigpr * np.log(eigv[...,None,:]) @ np.linalg.inv(eigpr)

    # Rotate strain to corotational material csys and convert to voigt
    strain = _subroutines.RotateTensor(strain,rot,rotm,
                                       ne,dof,ndi,nshr,ntens,nf,
                                       dir=-1,voigt=1,eng=1)

    return strain,rot,dfgrd