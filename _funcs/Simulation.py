import os
import numpy as np

import _funcs

def simulation(strain,rot,dfgrd,rotm,force,vol,vfs,ne,dof,ndi,nshr,ntens,
               nstatev,nvfs,nf,nt,nprops,props,nlgeom):
    """
    Simulation

    Parameters
    ----------
    strain : (nf,ne,ntens) , float
        Strain in corotational material csys.
    rot : (nf,ne,dof,dof) , float
        Rotation tensor.
    dfgrd : (nf,ne,dof,dof) , float
        Deformation gradient.
    rotm : (dof,dof) , float
        Material rotation tensor.
    force : (nf,dof) , float
        Global loading force.
    vol : (ne,) , float
        Elements volume.
    vfs : {(nvfs,ne,dof,dof), (nvfs,nn,dof)} , float
        User defined virtual fields.
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
    nlgeom : bool
        Flag for small or large deformation framework (0/1).

    Returns
    -------
    ivw : (nt,(nf,nvfs)) , float
        Internal virtual work.
    evw : (nt,(nf,nvfs)) , float
        External virtual work.
    res : (nt,(nf*nvfs,)) , float
        Cost function residuals for time increments and virtual fields.
    phi : (nt,) , float
        Cost function.
    """

    # Virtual fields method core function
    ivw,evw,res,phi = [None]*nt,[None]*nt,[None]*nt,[None]*nt
    for t in range(nt):
        ivw[t],evw[t],res[t],phi[t] = _funcs.vfm_core(strain[t],rot[t],
                                                        dfgrd[t],rotm[t],
                                                        force[t],vol[t],
                                                        vfs[t],ne[t],dof[t],
                                                        ndi[t],nshr[t],
                                                        ntens[t],nstatev[t],
                                                        nvfs[t],nf[t],nprops,
                                                        props,nlgeom)

        # Export reference force
        # name = 'Double-Notched-2D'
        # filename = f'input\{name}\{name}_Force.csv'
        # oldforce = np.loadtxt(filename,skiprows=1,delimiter=';')
        # oldforce[:,2] = ivw[t][:,0]/2
        # os.rename(filename,f'input\{name}\{name}_ForceFEM.csv')
        # with open(filename,'w') as f:
        #     if dof == 2:
        #         f.write('Time;X;Y\n')
        #     if dof == 3: 
        #         f.write('Time;X;Y;Z\n')
        #     np.savetxt(f,oldforce,delimiter=';')

    return res,phi