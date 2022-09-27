import sys
import numpy as np

import _funcs
import _utils

def VFM(prjnm):

    ##################
    # PRE-PROCESSING #
    ##################

    # Load options
    run,test,fout,tol,maxiter,props,vars,bounds,constr,nlgeom,vfs,bc,nprops,nvars,nt = _funcs.load_options(prjnm)

    # Create output directory
    dirout = _funcs.create_directory(prjnm,fout,test,nt)

    # Print start info to log file and return start time
    st = _funcs.print_start(prjname,fout,dirout)

    # Load project data
    coord,displ,conn,centr,force,time,thk,ori,nf = _funcs.load_data(prjnm,test,
                                                                    nt)

    # Set dimensional mechanics variables
    nn,ne,npe,dof,ndi,nshr,ntens,ncomp,nstatev = _funcs.dim_vars(coord,conn,
                                                                 nt,nlgeom)

    # Compute material rotation tensor
    rotm = [None]*nt
    for t in range(nt):
        rotm[t] = _funcs.material_rotation(ori[t],dof[t])

    # Compute strain and deformation gradient
    strain,rot,dfgrd,vol = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    for t in range(nt):
        strain[t],rot[t],dfgrd[t],vol[t] = _funcs.log_strain(coord[t],displ[t],
                                                             conn[t],rotm[t],
                                                             thk[t],ne[t],
                                                             npe[t],dof[t],
                                                             ndi[t],ntens[t],
                                                             nf[t])

    # Get boundary conditions degrees of freedom
    bcdofs = [None]*nt
    for t in range(nt):
        if 'sb' in list(vfs[t].keys()):
            bcdofs[t] = _funcs.boundary_conditions(coord[t],nn[t],dof[t],
                                                   bc[t],t)

    # Compute elements strain-displacement matrix
    bg,mbginv = [None]*nt,[None]*nt
    for t in range(nt):
        if 'sb' in list(vfs[t].keys()):
            bg[t],mbginv[t] = _funcs.strain_displacement(coord[t],conn[t],
                                                         bcdofs[t],nn[t],ne[t],
                                                         npe[t],dof[t],
                                                         ncomp[t],nlgeom)

    # Select type of virtual fields
    nvfs = [None]*nt
    for t in range(nt):

        # User-defined virtual fields
        if 'ud' in list(vfs[t].keys()):

            # Generate user-defined virtual fields
            vfs[t],nvfs[t],vfsu = _funcs.user_defined_virtual_fields(coord[t],
                                                                centr[t],nn[t],ne[t],
                                                                dof[t],vfs[t])

        # Sensitivity-based virtual fields
        elif 'sb' in list(vfs[t].keys()):

            # Number of sensitivity-based virtual fields
            nvfs[t] = nvars

            # Generate sensivity-based virtual fields
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

    ##############
    # PROCESSING #
    ##############

    # Simulate vfm with given material properties
    if run == 'simulation':

        # Apply user-defined properties constraints
        if len(constr) > 0:
            props = _funcs.properties_constraints(props,constr)

        layers = [[[],[],[]]]*nt
        if dof[0] == 3:
            coordpel = [None]*nt
            coordpel[0] = coord[0][conn[0]]

            for i in range(ne[0]):
                zcoords = 2 * np.unique(coordpel[0][i,:,2]) / thk[0]
                if -1 in zcoords:
                    layers[0][0].append(i)
                elif 1 in zcoords:
                    layers[0][2].append(i)
                else:
                    layers[0][1].append(i)

        # Perform vfm simulation with given material properties
        ivw,evw,phi,success = _funcs.simulation(strain,rot,dfgrd,rotm,force,
                                                vol,vfs,ne,dof,ndi,nshr,ntens,
                                                nstatev,nvfs,nf,nt,nprops,
                                                props,nlgeom,fout)

        # Write virtual work of given material properties
        for t in range(nt):
            _funcs.write_virtual_work(ivw[t],evw[t],test[t],nvfs[t],nf[t],
                                      nt,fout,dirout)

        # Print summary of simulation results to log
        _funcs.print_result_simulation(phi,nt,fout,dirout,st)

    # Perform identification of material properties
    elif run == 'identification':

        props = _funcs.identification(strain,rot,dfgrd,rotm,force,time,vol,bg,
                                      mbginv,bcdofs,vfs,nn,ne,dof,ndi,nshr,
                                      ntens,ncomp,nstatev,nvfs,nf,nt,nprops,
                                      nvars,props,vars,bounds,constr,nlgeom,
                                      test,fout,dirout,tol,maxiter,st)

    ###################
    # POST-PROCESSING #
    ###################

    # Loop over tests
    for t in range(nt):
        _funcs.post_processing(coord[t],displ[t],conn[t],strain[t],rot[t],
                               dfgrd[t],vol[t],time[t],rotm[t],vfs[t],ne[t],
                               dof[t],ndi[t],nshr[t],ntens[t],ncomp[t],
                               nstatev[t],nvfs[t],nf[t],test[t],nt,nprops,
                               props,vars,nlgeom,fout,dirout,vfsu)

    return

if __name__ == '__main__':

    # Clear command window
    _utils.clear_screen()

    # Name of project
    prjname = 'Debug-3D'

    # Name of project from command line
    if len(sys.argv) > 1:
        prjname = sys.argv[-1]

    VFM(prjname)