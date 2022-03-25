import _funcs

def VFM(prjnm):

    ##################
    # PRE-PROCESSING #
    ##################

    # Load options
    run,props,vars,bounds,constr,nlgeom,algo,nprops,nvars,nt,options = _funcs.load_options(prjnm)

    # Create output directory
    _funcs.create_directory(prjnm,options.fout,options.tests,nt)

    # Load project data
    coord,displ,conn,centr,force,thick,ori,nf = _funcs.load_data(prjnm,
                                                                 options.tests,
                                                                 nt)

    # Set dimensional variables
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
                                                            options.ivfs[t])

    ##############
    # PROCESSING #
    ##############

    # Simulate vfm with given material properties
    if run == 'simulation':
        res,phi = _funcs.simulation(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,
                                    ndi,nshr,ntens,nstatev,nvfs,nf,nt,nprops,
                                    props,nlgeom)

    # Perform identification of material properties
    elif run == 'identification':
        props = _funcs.identification(strain,rot,dfgrd,rotm,force,vol,vfs,ne,
                                      dof,ndi,nshr,ntens,nstatev,nvfs,nf,nt,
                                      nprops,nvars,props,vars,bounds,constr,
                                      nlgeom,algo,options.fout)

    ###################
    # POST-PROCESSING #
    ###################


    stress,statev,d33,pkstress = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    for t in range(nt):

        # Compute cauchy stress of best solution
        stress[t],statev[t],d33[t] = _funcs.cauchy_stress(strain[t],rot[t],
                                                          rotm[t],ne[t],dof[t],
                                                          ndi[t],nshr[t],
                                                          ntens[t],nstatev[t],
                                                          nf[t],nprops,props,
                                                          voigt=0)

        # Compute 1st piola-kirchhoff stress
        pkstress[t] = _funcs.piola_kirchhoff_stress(stress[t],d33[t],dfgrd[t],
                                                    dof[t])

        # Rotate strain to global csys
        strain[t] = _funcs.rotate_tensor(strain[t],rot[t],rotm[t],ne[t],dof[t],
                                         ndi[t],nshr[t],ntens[t],nf[t],
                                         dir=1,voigt=0,eng=0)

        # Export model to paraview
        _funcs.export_paraview(coord[t],displ[t],conn[t],strain[t],vol[t],
                               stress[t],statev[t],d33[t],pkstress[t],vfs[t],
                               ne[t],dof[t],nvfs[t],nf[t],nt,options.fout,
                               options.tests[t])

    return

if __name__ == '__main__':

    prjname = 'Double-Notched-vonMises'

    VFM(prjname)