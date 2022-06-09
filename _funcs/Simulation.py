import _funcs

def simulation(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,
               nstatev,nvfs,nf,nt,nprops,props,nlgeom,fout):
    """
    Simulation

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
    vol : (nt, (ne) ) , float
        Elements volume.
    vfs : (nt, {'e': (nvfs,ne,dof*dof), 'u': (nvfs,nn,dof)} ) , float
        Settings and generated virtual fields.
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
    nstatev : (nt) , int
        Number of internal state variables.
    nvfs : (nt) , int
        Number of virtual fields.
    nf : (nt) , int
        Number of increments.
    nprops : int
        Number of material properties.
    props : (nprops) , float
        Material properties.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    fout : str
        Name of output folder.

    Returns
    -------
    ivw : (nt, (nf,nvfs) ) , float
        Internal virtual work.
    evw : (nt, (nf,nvfs) ) , float
        External virtual work.
    phi : (nt) , float
        Cost function.

    Notes
    -----
    npe : int
        Number of nodes per element.
    """

    ivw,evw,phi,success = [None]*nt,[None]*nt,[None]*nt,[None]*nt

    # Loop over tests
    for t in range(nt):

        # Compute the principle of virtual work
        ivw[t],evw[t],phi[t],success = _funcs.vfm_core(strain[t],rot[t],
                                                       dfgrd[t],rotm[t],
                                                       force[t],vol[t],vfs[t],
                                                       ne[t],dof[t],ndi[t],
                                                       nshr[t],ntens[t],
                                                       nstatev[t],nvfs[t],
                                                       nf[t],nprops,props,
                                                       nlgeom,fout)

        # Break loop if one test is not successful reconstructed
        if not success:
            break

    return ivw,evw,phi,success