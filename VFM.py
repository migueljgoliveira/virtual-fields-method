import _funcs

def VFM(prjnm):

    ##################
    # PRE-PROCESSING #
    ##################

    # Load options
    run,tests,fout,props,vars,bounds,constr,nlgeom,symm,algo,ivfs,bc,nprops,nvars,nt = _funcs.load_options(prjnm)

    # Create output directory
    _funcs.create_directory(prjnm,fout,tests,nt)

    # Load project data
    coord,displ,conn,centr,force,time,thick,ori,nf = _funcs.load_data(prjnm,
                                                                      tests,
                                                                      symm,nt)

    # Set dimensional mechanics variables
    nn,ne,npe,dof,ndi,nshr,ntens,ncomp,nstatev = _funcs.dim_vars(coord,conn,nt,
                                                                 nlgeom)

    # Compute material rotation tensor
    rotm = [None]*nt
    for t in range(nt):
        rotm[t] = _funcs.material_rotation(ori[t],dof[t])

    # Compute strain and deformation gradient
    strain,rot,dfgrd,vol = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    for t in range(nt):
        strain[t],rot[t],dfgrd[t],vol[t] = _funcs.log_strain(coord[t],displ[t],
                                                             conn[t],rotm[t],
                                                             thick[t],ne[t],
                                                             npe[t],dof[t],
                                                             ndi[t],nshr[t],
                                                             ntens[t],nf[t])

    # Get boundary conditions degrees of freedom
    bccte,bcfix,bcact = [None]*nt,[None]*nt,[None]*nt
    for t in range(nt):
        if list(ivfs[t].keys())[0] == 'sb':
            bccte[t],bcfix[t],bcact[t] = _funcs.boundary_conditions(coord[t],
                                                                    nn[t],
                                                                    dof[t],
                                                                    bc[t],t)

    # Compute elements strain-displacement matrix
    bg,mbginv,ielems = [None]*nt,[None]*nt,[None]*nt
    for t in range(nt):
        if list(ivfs[t].keys())[0] == 'sb':
            bg[t],mbginv[t],ielems[t] = _funcs.strain_displacement(coord[t],
                                                                   conn[t],
                                                                   bcfix[t],
                                                                   nn[t],ne[t],
                                                                   npe[t],
                                                                   dof[t],
                                                                   ncomp[t],
                                                                   nlgeom)

    # Select type of virtual fields
    vfs,nvfs = [None]*nt,[None]*nt,
    for t in range(nt):

        # User-defined virtual fields
        if list(ivfs[t].keys())[0] == 'ud':
            vfs[t],nvfs[t] = _funcs.user_defined_virtual_fields(coord[t],
                                                                centr[t],
                                                                ne[t],dof[t],
                                                                ivfs[t])

        # Sensitivity-based virtual fields
        elif list(ivfs[t].keys())[0] == 'sb':

            # Number of sensitivity-based virtual fields
            nvfs[t] = nvars


    ##############
    # PROCESSING #
    ##############

    # Simulate vfm with given material properties
    if run == 'simulation':

        # Apply user-defined properties constraints
        if len(constr) > 0:
            props = _funcs.properties_constraints(props,constr)

        _,_,res,phi = _funcs.simulation(strain,rot,dfgrd,rotm,force,time,vol,
                                        bg,mbginv,bccte,bcact,ielems,vfs,nn,ne,
                                        npe,dof,ndi,nshr,ntens,ncomp,nstatev,
                                        nvfs,nf,nt,nprops,props,vars,nlgeom,
                                        symm,ivfs,tests,fout)

    # Perform identification of material properties
    elif run == 'identification':

        props = _funcs.identification(strain,rot,dfgrd,rotm,force,time,vol,bg,
                                      mbginv,bccte,bcact,ielems,vfs,nn,ne,npe,
                                      dof,ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,
                                      nt,nprops,nvars,props,vars,bounds,constr,
                                      nlgeom,symm,ivfs,algo,tests,fout)

    ###################
    # POST-PROCESSING #
    ###################

    stress,statev,de33,pkstress = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    pstrain = [None]*nt
    for t in range(nt):

        # Compute cauchy stress of best solution
        stress[t],statev[t],de33[t] = _funcs.cauchy_stress(strain[t],rot[t],
                                                           rotm[t],ne[t],
                                                           dof[t],ndi[t],
                                                           nshr[t],ntens[t],
                                                           nstatev[t],nf[t],
                                                           nprops,props,fout,
                                                           voigt=0)

        # Compute 1st piola-kirchhoff stress
        pkstress[t] = _funcs.piola_kirchhoff_stress(stress[t],de33[t],dfgrd[t],
                                                    ne[t],dof[t],nf[t],flat=0)

        # Rotate strain to global csys
        strain[t] = _funcs.rotate_tensor(strain[t],rot[t],rotm[t],ne[t],dof[t],
                                         ndi[t],nshr[t],ntens[t],nf[t],
                                         dir=1,voigt=0,eng=1)

        # Convert plastic strain to tensor form
        pstrain[t] = _funcs.voigt_to_tensor(statev[t][...,1:],ne[t],dof[t],
                                            ndi[t],nshr[t],ntens[t],nf[t],
                                            eng=1)

        # Reshape virtual fields to tensor format
        vfs[t]['e'] = _funcs.reshape_tensor(vfs[t]['e'],ne[t],dof[t],nf[t],-1,
                                            nvfs[t])

        # Export model of best solution to paraview
        _funcs.export_paraview(coord[t],displ[t],conn[t],strain[t],vol[t],
                               stress[t],statev[t][...,0],pstrain[t],de33[t],
                               pkstress[t],vfs[t],dof[t],nvfs[t],nf[t],
                               tests[t],nt,fout)

    return

if __name__ == '__main__':

    # Clear command window
    _funcs.clear_screen()

    # Name of project
    prjname = 'Double-Notched-2D'

    VFM(prjname)