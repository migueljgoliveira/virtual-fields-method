import _funcs

def simulation(strain,rot,dfgrd,rotm,force,time,vol,bg,mbginv,bccte,bcact,
               ielems,vfs,nn,ne,npe,dof,ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,
               nt,nprops,props,vars,nlgeom,symm,ivfs,tests,fout):
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
    time : (nt, (nf,) ) , float
        Time increments.
    vol : (nt, (ne,) ) , float
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
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        Material properties.
    vars : (nprops,) , bool
        Flags for identification variables.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    ivfs : (nt, {'ud' or 'sb'} ) , int
        List of selected virtual fields.
    symm : (nt, (nsymm,) ), int
        List of symmetry conditions.
    tests : (nt,) , str
        List of tests name.
    fout : str
        Name of output folder.

    Returns
    -------
    ivw : (nt, (nf,nvfs) ) , float
        Internal virtual work.
    evw : (nt, (nf,nvfs) ) , float
        External virtual work.
    res : (nt, (nf*nvfs,) ) , float
        Cost function residuals for time increments and virtual fields.
    phi : (nt,) , float
        Cost function.

    Notes
    -----
    nbcact : int
        Number of active degrees of freedom.
    """

    ivw,evw,res,phi = [None]*nt,[None]*nt,[None]*nt,[None]*nt

    # Loop over tests
    for t in range(nt):

        # Generate sensivity-based virtual fields
        if list(ivfs[t].keys())[0] == 'sb':
            vfs[t] = _funcs.sensivity_based_virtual_fields(strain[t],rot[t],
                                                           dfgrd[t],rotm[t],
                                                           time[t],bg[t],
                                                           mbginv[t],ielems[t],
                                                           bccte[t],bcact[t],
                                                           nn[t],ne[t],
                                                           dof[t],ndi[t],
                                                           nshr[t],ntens[t],
                                                           ncomp[t],nstatev[t],
                                                           nvfs[t],nf[t],
                                                           nprops,props,vars,
                                                           ivfs[t]['sb'],
                                                           nlgeom,fout)

        # Compute the principle of virtual work
        ivw[t],evw[t],res[t],phi[t] = _funcs.vfm_core(strain[t],rot[t],
                                                      dfgrd[t],rotm[t],
                                                      force[t],vol[t],vfs[t],
                                                      ne[t],dof[t],ndi[t],
                                                      nshr[t],ntens[t],
                                                      nstatev[t],nvfs[t],nf[t],
                                                      symm[t],nprops,props,
                                                      nlgeom,fout)

        # Write virtual work of current solution
        _funcs.write_virtual_work(ivw[t],evw[t],tests[t],nvfs[t],nf[t],nt,fout)

    return ivw,evw,res,phi