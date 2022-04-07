import _funcs

def VFM(prjnm):

    ##################
    # PRE-PROCESSING #
    ##################

    # Load options
    run,tests,fout,props,vars,bounds,constr,nlgeom,symm,algo,ivfs,nprops,nvars,nt = _funcs.load_options(prjnm)

    # Create output directory
    _funcs.create_directory(prjnm,fout,tests,nt)

    # Load project data
    coord,displ,conn,centr,force,thick,ori,nf = _funcs.load_data(prjnm,tests,
                                                                 symm,nt)

    # Set dimensional mechanics variables
    nn,ne,npe,dof,ndi,nshr,ntens,nstatev = _funcs.dim_vars(coord,conn,nt)

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

    # Generate user defined virtual fields
    vfs,nvfs = [None]*nt,[None]*nt
    for t in range(nt):
        vfs[t],nvfs[t] = _funcs.user_defined_virtual_fields(coord[t],centr[t],
                                                            ne[t],dof[t],
                                                            ivfs[t])

    ##############
    # PROCESSING #
    ##############

    # Simulate vfm with given material properties
    if run == 'simulation':

        # Apply user-defined properties constraints
        if len(constr) > 0:
            props = _funcs.properties_constraints(props,constr)

        res,phi = _funcs.simulation(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,
                                    ndi,nshr,ntens,nstatev,nvfs,nf,nt,nprops,
                                    props,nlgeom,symm)

    # Perform identification of material properties
    elif run == 'identification':
        props = _funcs.identification(strain,rot,dfgrd,rotm,force,vol,vfs,ne,
                                      dof,ndi,nshr,ntens,nstatev,nvfs,nf,nt,
                                      nprops,nvars,props,vars,bounds,constr,
                                      nlgeom,symm,algo,fout)

    ###################
    # POST-PROCESSING #
    ###################

    stress,statev,de33,pkstress = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    for t in range(nt):

        # Compute cauchy stress of best solution
        stress[t],statev[t],de33[t] = _funcs.cauchy_stress(strain[t],rot[t],
                                                           rotm[t],ne[t],
                                                           dof[t],ndi[t],
                                                           nshr[t],ntens[t],
                                                           nstatev[t],nf[t],
                                                           nprops,props,
                                                           voigt=0)

        # Compute 1st piola-kirchhoff stress
        pkstress[t] = _funcs.piola_kirchhoff_stress(stress[t],de33[t],dfgrd[t])

        # Rotate strain to global csys
        strain[t] = _funcs.rotate_tensor(strain[t],rot[t],rotm[t],ne[t],dof[t],
                                         ndi[t],nshr[t],ntens[t],nf[t],
                                         dir=1,voigt=0,eng=0)

        # Export model to paraview
        _funcs.export_paraview(coord[t],displ[t],conn[t],strain[t],vol[t],
                               stress[t],statev[t],de33[t],pkstress[t],vfs[t],
                               ne[t],dof[t],nvfs[t],nf[t],nt,fout,tests[t])

    return

if __name__ == '__main__':

    # Clear command window
    _funcs.clear_screen()

    # Name of project
    prjname = 'Butterfly-SEM'

    VFM(prjname)