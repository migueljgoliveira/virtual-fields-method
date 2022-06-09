import numpy as np

import _funcs

def sensivity_based_virtual_fields(strain,rot,dfgrd,rotm,time,bg,mbginv,bcdofs,
                                   vfs,nn,ne,dof,ndi,nshr,ntens,ncomp,nstatev,
                                   nvfs,nf,nprops,props,vars,nlgeom,fout):
    """
    Compute the sensitivity-based virtual fields.

    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    rotm : (dof,dof) , float
        Material rotation tensor.
    time : (nf) , float
        Time increments.
    bg : (ne*ncomp,nn*dof) , float
        Global strain-displacement matrix.
    mbginv : (ne*ncomp,nn*dof) , float
        Pseudo-inverse of modified global strain-displacement matrix.
    bcdofs : {'fixed','active','parent','child'} , int
        Boundary conditions degrees of freedom.
    vfs : 
        Settings and generated virtual fields.
    nn : int
        Number of nodes.
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
    nvfs : int
        Number of virtual fields.
    nf : int
        Number of increments.
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Material properties.
    vars : (nprops,) , bool
        Flags for identification variables.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    fout : str
        Name of output folder.

    Returns
    -------
    vfs : {(nvfs,ne,dof*dof), (nvfs,nf,4,dof)} , float
        Sensivity-based virtual fields.
    """

    # Compute stress sensitivities
    ss,iss = _funcs.stress_sensitivity(strain,rot,dfgrd,rotm,time,
                                       vfs['sb']['dx'],ne,dof, ndi,nshr,ntens,
                                       ncomp,nstatev,nf,nprops,props,vars,nvfs,
                                       nlgeom,fout)

    # Compute virtual displacements
    vu = np.zeros((nvfs,nf,nn*dof,1))
    vu[...,bcdofs['active'],:] = mbginv[None,None] @ iss[...,None]

    # Apply constant boundary conditions to virtual displacements
    for i in range(4):
        for j in range(dof):
            if len(bcdofs['parent'][i][j]) > 0:
                mastervu = vu[...,bcdofs['parent'][i][j][0],:]
                vu[...,bcdofs['child'][i][j],0] = mastervu

    # Compute virtual strains
    ve = bg[None,None] @ vu

    # Reshape virtual displacements to virtual fields format
    vfs['u'] = np.zeros((nvfs,nf,4,dof))
    for i in range(4):
        for j in range(dof):
            if len(bcdofs['parent'][i][j]) > 0:
                vfs['u'][...,i,j] = vu[...,bcdofs['parent'][i][j][0],0]

    # Reshape virtual strains to virtual fields format
    ielems = np.arange(0,ne*dof*dof).reshape(dof*dof,ne).T
    vfs['e'] = ve[...,ielems,:][...,0]

    return vfs