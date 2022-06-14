import numpy as np

import _funcs
import _utils

def post_processing(coord,displ,conn,strain,rot,dfgrd,vol,time,rotm,vfs,ne,dof,
                    ndi,nshr,ntens,ncomp,nstatev,nvfs,nf,test,nt,nprops,props,
                    vars,nlgeom,fout,dirout):
    """
    Post-processing of best solution data and export. 

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    displ : (nf,nn,dof) , float
        Nodes displacements.
    conn : (ne,npe) , int
        Elements connectivity.
    strain : (nf,ne,ntens) , float
        Strain in global csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    vol : (ne) , float
        Elements volume.
    time : (nf,) , float
        Time increments.
    rotm : (dof,dof) , float
        Material rotation tensor.
    vfs : {(nvfs,ne,dof,dof), (nvfs,nn,dof)} , float
        Settings and generated virtual fields.
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
    ivfs : {'ud' or 'sb'} , dict
        List of selected virtual fields.
    test : str
        Name of test.
    nt : int
        Number of tests.
    nprops : int
        Number of material properties.
    props : (nprops) , float
        Material properties.
    vars : (nprops,) , bool
        Flags for identification variables.
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    fout : str
        Name of output folder.
    dirout : str
        Directory of project to export output files.
    """

    # Compute stress sensitivities of best solution
    ss,iss = None,None
    if 'sb' in list(vfs.keys()):
        ss,iss = _funcs.stress_sensitivity(strain,rot,dfgrd,rotm,time,
                                           vfs['sb']['dx'],ne,dof,ndi,nshr,
                                           ntens,ncomp,nstatev,nf,nprops,
                                           props,vars,nvfs,nlgeom,fout,0)

    # Compute cauchy stress of best solution
    stress,statev,de33,_ = _funcs.cauchy_stress(strain,rot,rotm,ne,dof,ndi,
                                                nshr,ntens,nstatev,nf,nprops,
                                                props,fout,voigt=False)

    # Rotate plastic strain to global csys
    pstrain = _utils.rotate_tensor(statev[...,1:],rot,rotm,ne,dof,ndi,
                                   ntens,nf,dir=1,voigt=True,eng=True)

    # Compute 1st piola-kirchhoff stress of best solution
    pkstress = _funcs.piola_kirchhoff_stress(stress,de33,dfgrd,ne,dof,
                                             nf,flat=False)

    # Convert cauchy stress to voigt form
    stress = _utils.tensor_to_voigt(stress,ne,ndi,ntens,nf)

    # Rotate strain to global csys
    strain = _utils.rotate_tensor(strain,rot,rotm,ne,dof,ndi,ntens,nf,
                                  dir=1,voigt=True,eng=True)

    # Export model of best solution to paraview
    _funcs.export_paraview(coord,displ,conn,strain,vol,stress,statev[...,0],
                           pstrain,de33,pkstress,vfs,ss,iss,ne,dof,nvfs,nf,
                           test,nt,fout,dirout)

    return