import _subroutines

def InternalVirtualWork(strain,rot,dfgrd,rotm,
                        props,nprops,
                        ne,dof,ndi,nshr,ntens,nstatev,nf):

    # Compute cauchy stress on corotational material csys
    stress,d33 = _subroutines.CauchyStress(strain,
                                           props,nprops,
                                           ne,ndi,nshr,ntens,nstatev,nf)

    # Rotate cauchy stress to global csys
    stress = _subroutines.RotateTensor(stress,rot,rotm,
                                       ne,dof,ndi,nshr,ntens,nf,
                                       dir=1,voigt=0)

    # Compute 1st piola-kirchhoff stress on global csys
    pkstress = _subroutines.PiolaKirchhoffStress(stress,d33,dfgrd,dof)

    # return ivw