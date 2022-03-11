import numpy as np

import _funcs

def VFM(prjname,out,lvfs):

    ##################
    # PRE-PROCESSING #
    ##################

    # Load settings
    props,opti,bounds,constr,nprops,nlgeom = _funcs.load_settings(prjname)

    # Create output directory
    _funcs.create_directory(out)

    # Load geometry data
    coord,displ,conn,centroid,force,thick,ori,nf = _funcs.load_data(prjname)

    # Set dimensional variables
    nn,ne,npe,dof,ndi,nshr,ntens,nstatev,nvfs = _funcs.dim_vars(coord,conn,
                                                                lvfs)

    # Compute material rotation tensor
    rotm = _funcs.material_rotation(ori,dof)

    # Compute strain and deformation gradient
    strain,rot,dfgrd,vol = _funcs.log_strain(coord[conn],displ[:,conn],rotm,
                                             thick,ne,npe,dof,ndi,nshr,
                                             ntens,nf)

    # Generate user defined virtual fields
    vfs = _funcs.user_defined_virtual_fields(coord,centroid,ne,dof,lvfs,nvfs)

    ##################
    # IDENTIFICATION #
    ##################

    _funcs.identification(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,
                          ntens,nstatev,nvfs,nf,props,opti,bounds,constr,
                          nprops,nlgeom)

    # ivw,evw,res,phi = _funcs.vfm_core(strain,rot,dfgrd,rotm,force,vol,
    #                                        vfs,props,nprops,ne,dof,ndi,nshr,
    #                                        ntens,nstatev,nvfs,nf,nlgeom)

    ###################
    # POST-PROCESSING #
    ###################

    # Compute cauchy stress on corotational material csys in voigt form
    stress,statev,d33 = _funcs.cauchy_stress(strain,rot,rotm,props,ne,dof,ndi,
                                             nshr,ntens,nstatev,nf,voigt=1)


    # Rotate strain to global csys
    strain = _funcs.rotate_tensor(strain,rot,rotm,ne,dof,ndi,nshr,ntens,nf,
                                  dir=1,voigt=1,eng=0)

    # Export model to paraview
    _funcs.export_paraview(coord,displ,conn,strain,stress,statev,d33,vfs,dof,
                           nf,nvfs,out,folder='output')

    return

if __name__ == '__main__':

    name = 'Double-Notched-2D'
    output = name

    # Set type of user defined virtual fields
    lvfs = np.array([1,3,4])

    VFM(name,output,lvfs)