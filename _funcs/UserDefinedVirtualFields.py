import numpy as np
from numpy import pi,sin,cos,sign

def user_defined_virtual_fields(coord,centr,nn,ne,dof,vfs):
    """
    Generate user-defined virtual fields.

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    centr : (ne,dof) , float
        Elements centroid reference coordinates.
    ne : int
        Number of elements.
    dof : int
        Number of degrees of freedom.
    ivfs : {(nt,nvfs)} , int
        List of user-defined virtual fields. 

    Returns
    -------
    vfs : {(nvfs,ne,dof*dof), (nvfs,nn,dof)} , float
        User-defined virtual fields.
    nvfs : int
        Number of virtual fields.

    Notes
    -----
    nn : int
        Number of nodes.

    The virtual strains are stored in flat format according to:

        2D
            vfs['e'][...,0] = xx
            vfs['e'][...,1] = yy

            vfs['e'][...,2] = xy
            vfs['e'][...,3] = yx

        3D
            vfs['e'][...,0] = xx
            vfs['e'][...,1] = yy
            vfs['e'][...,2] = zz

            vfs['e'][...,3] = xy
            vfs['e'][...,4] = yx

            vfs['e'][...,5] = xz
            vfs['e'][...,6] = zx

            vfs['e'][...,7] = yz
            vfs['e'][...,8] = zy
    """

    # Number of user-defined virtual fields
    nvfs = len(vfs['ud'])

    # Compute half-width, half-height and half-thickness of geometry
    if dof == 2:
        w,h = np.max(coord,0)
    elif dof == 3:
        w,h,t = np.max(coord,0)

    # Create nodes coordinate and elements centroid variables
    if dof == 2:
        xn,yn = coord[:,0],coord[:,1]
        xe,ye = centr[:,0],centr[:,1]
    elif dof == 3:
        xn,yn,zn = coord[:,0],coord[:,1],coord[:,2]
        xe,ye,ze = centr[:,0],centr[:,1],centr[:,2]

    # Compute maximum edge boundary coordinates
    xu,yu,zu = np.max(xn),np.max(yn),0

    # Create variables to store virtual fields
    vfs['e'] = np.zeros((nvfs,1,ne,dof*dof))
    vfs['u'] = np.zeros((nvfs,1,dof))
    vfsu = np.zeros((nvfs,1,nn,dof))

    # Generate user-defined virtual fields

    # 2D
    if dof == 2:
        i = 0
        for ivf in vfs['ud']:

            # Type 1
            if ivf == 1:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = yu / h

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = 1 / h
                vfs['e'][i,...,2] = 0
                vfs['e'][i,...,3] = 0

            # Type 2
            if ivf == 2:
                vfs['u'][i,:,0] = 1/pi * sin(pi*xu/w) * cos(0.5*pi*yu/h)
                vfs['u'][i,:,1] = 1/pi * sin(pi*xu/w) * cos(0.5*pi*yu/h)

                vfs['e'][i,...,0] =    1/w * cos(pi*xe/w) * cos(0.5*pi*ye/h)
                vfs['e'][i,...,1] = -0.5/h * sin(pi*xe/w) * sin(0.5*pi*ye/h)

                vfs['e'][i,...,2] = -0.5/h * sin(pi*xe/w) * sin(0.5*pi*ye/h)
                vfs['e'][i,...,3] =    1/w * cos(pi*xe/w) * cos(0.5*pi*ye/h)


            i += 1

    # 3D
    if dof == 3:
        i = 0
        for ivf in vfs['ud']:

            # Type 1
            if ivf == 1:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = yu / h
                vfs['u'][i,:,2] = 0

                vfsu[i,...,0] = 0
                vfsu[i,...,1] = yn / h
                vfsu[i,...,2] = 0

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = 1 / h
                vfs['e'][i,...,2] = 0

                vfs['e'][i,...,3] = 0
                vfs['e'][i,...,4] = 0

                vfs['e'][i,...,5] = 0
                vfs['e'][i,...,6] = 0

                vfs['e'][i,...,7] = 0
                vfs['e'][i,...,8] = 0

            # Type 2
            if ivf == 2:
                vfs['u'][i,:,0] = 1/pi * sin(pi*xu/w) * cos(0.5*pi*yu/h)
                vfs['u'][i,:,1] = 1/pi * sin(pi*xu/w) * cos(0.5*pi*yu/h)
                vfs['u'][i,:,2] = 0

                vfsu[i,...,0] = 1/pi * sin(pi*xn/w) * cos(0.5*pi*yn/h)
                vfsu[i,...,1] = 1/pi * sin(pi*xn/w) * cos(0.5*pi*yn/h)
                vfsu[i,...,2] = 0

                vfs['e'][i,...,0] =    1/w * cos(pi*xe/w) * cos(0.5*pi*ye/h)
                vfs['e'][i,...,1] = -0.5/h * sin(pi*xe/w) * sin(0.5*pi*ye/h)
                vfs['e'][i,...,2] = 0

                vfs['e'][i,...,3] = -0.5/h * sin(pi*xe/w) * sin(0.5*pi*ye/h)
                vfs['e'][i,...,4] =    1/w * cos(pi*xe/w) * cos(0.5*pi*ye/h)

                vfs['e'][i,...,5] = 0
                vfs['e'][i,...,6] = 0

                vfs['e'][i,...,7] = 0
                vfs['e'][i,...,8] = 0

            # Type 3
            if ivf == 3:
                vfs['u'][i,:,0] = 1/pi * ( sin(pi*xu/w) *
                                           cos(0.5*pi*yu/h) *
                                           cos(0.5*pi*zu/t) )
                vfs['u'][i,:,1] = 1/pi * ( sin(pi*xu/w) *
                                           cos(0.5*pi*yu/h) *
                                           cos(0.5*pi*zu/t) )
                vfs['u'][i,:,2] = 1/pi * ( sin(pi*xu/w) *
                                           cos(0.5*pi*yu/h) *
                                           sin(0.5*pi*zu/t) )


                vfsu[i,...,0] = 1/pi * ( sin(pi*xn/w) *
                                           cos(0.5*pi*yn/h) *
                                           cos(0.5*pi*zn/t) )
                vfsu[i,...,1] = 1/pi * ( sin(pi*xn/w) *
                                           cos(0.5*pi*yn/h) *
                                           cos(0.5*pi*zn/t) )
                vfsu[i,...,2] = 1/pi * ( sin(pi*xn/w) *
                                           cos(0.5*pi*yn/h) *
                                           sin(0.5*pi*zn/t) )

                vfs['e'][i,...,0] =    1/w * ( cos(pi*xe/w) *
                                               cos(0.5*pi*ye/h) *
                                               cos(0.5*pi*ze/t) )
                vfs['e'][i,...,1] = -0.5/h * ( sin(pi*xe/w) *
                                               sin(0.5*pi*ye/h) *
                                               cos(0.5*pi*ze/t) )
                vfs['e'][i,...,2] =  0.5/t * ( sin(pi*xe/w) *
                                               cos(0.5*pi*ye/h) *
                                               cos(0.5*pi*ze/t) )

                vfs['e'][i,...,3] = -0.5/h * ( sin(pi*xe/w) *
                                               sin(0.5*pi*ye/h) *
                                               cos(0.5*pi*ze/t) )
                vfs['e'][i,...,4] =    1/w * ( cos(pi*xe/w) *
                                               cos(0.5*pi*ye/h) *
                                               cos(0.5*pi*ze/t) )

                vfs['e'][i,...,5] = -0.5/t * ( sin(pi*xe/w) *
                                               cos(0.5*pi*ye/h) *
                                               sin(0.5*pi*ze/t) )
                vfs['e'][i,...,6] =    1/w * ( cos(pi*xe/w) *
                                               cos(0.5*pi*ye/h) *
                                               sin(0.5*pi*ze/t) )

                vfs['e'][i,...,7] = -0.5/t * ( sin(pi*xe/w) *
                                               cos(0.5*pi*ye/h) *
                                               sin(0.5*pi*ze/t) )
                vfs['e'][i,...,8] = -0.5/h * ( sin(pi*xe/w) *
                                               sin(0.5*pi*ye/h) *
                                               sin(0.5*pi*ze/t) )

            i += 1

    # Check for absolute zero
    tol = 1e-16
    vfs['u'][abs(vfs['u']) < tol] = 0
    vfs['e'][abs(vfs['e']) < tol] = 0

    return vfs,nvfs,vfsu


# List of additional virtual fields

# 2D

# 1
# vfs['u'][i,:,0] = xu/w * (abs(yu)-h)/h
# vfs['u'][i,:,1] = 0
# vfs['e'][i,...,0] = (abs(ye)-h) / (w*h)
# vfs['e'][i,...,1] = 0
# vfs['e'][i,...,2] = sign(ye) * xe/(w*h)
# vfs['e'][i,...,3] = 0

# 2
# vfs['u'][i,:,0] = xu*(yu**2-yu*h) / (w*h**2)
# vfs['u'][i,:,1] = 0
# vfs['e'][i,...,0] = (ye**2-ye*h) / (w*h**2)
# vfs['e'][i,...,1] = 0
# vfs['e'][i,...,2] = xe*(2*ye-h) / (w*h**2)
# vfs['e'][i,...,3] = 0

# 3
# vfs['u'][i,:,0] = sin(pi*xu/w) * sin(pi*yu/h)
# vfs['u'][i,:,1] = 0
# vfs['e'][i,...,0] = pi/w * cos(pi*xe/w) * sin(pi*ye/h)
# vfs['e'][i,...,1] = 0
# vfs['e'][i,...,2] = pi/h * sin(pi*xe/w) * cos(pi*ye/h)
# vfs['e'][i,...,3] = 0

# 4
# vfs['u'][i,:,0] = 0
# vfs['u'][i,:,1] = sin(pi*xu/w) * sin(pi*yu/h)
# vfs['e'][i,...,0] = 0
# vfs['e'][i,...,1] = pi/h * sin(pi*xe/w) * cos(pi*ye/h)
# vfs['e'][i,...,2] = 0
# vfs['e'][i,...,3] = pi/w * cos(pi*xe/w) * sin(pi*ye/h)

# 5
# vfs['u'][i,:,0] = 0
# vfs['u'][i,:,1] = xu*(yu**2-yu*h) / (w*h**2)
# vfs['e'][i,...,0] = 0
# vfs['e'][i,...,1] = xe*(2*ye-h) / (w*h**2)
# vfs['e'][i,...,2] = 0
# vfs['e'][i,...,3] = (ye**2-ye*h) / (w*h**2)

# 6
# vfs['u'][i,:,0] = 0
# vfs['u'][i,:,1] = (yu**2*h-yu**3)/h**3 * sin(pi*xu/w)
# vfs['e'][i,...,0] = 0
# vfs['e'][i,...,1] = (2*h*ye-3*ye**2)/h**3 * sin(pi*xe/w)
# vfs['e'][i,...,2] = 0
# vfs['e'][i,...,3] = pi/(w*h**3)* (h*ye**2-ye**3) * cos(pi*xe/w)

# 7
# vfs['u'][i,:,0] = ((h**3-yu**3)/h**3) * sin(pi*xu/w)
# vfs['u'][i,:,1] = 0
# vfs['e'][i,...,0] = pi*(h**3-ye**3)/(w*h**3) * cos(pi*xe/w)
# vfs['e'][i,...,1] = 0
# vfs['e'][i,...,2] = - ((3*ye**2)/h**3) * sin(pi*xe/w)
# vfs['e'][i,...,3] = 0

# 8
# vfs['u'][i,:,0] = 0
# vfs['u'][i,:,1] = (yu*h**2-yu**3)/h**3 * sin(pi*xu/w)
# vfs['e'][i,...,0] = 0
# vfs['e'][i,...,1] = (h**2-3*ye**2)/h**3 * sin(pi*xe/w)
# vfs['e'][i,...,2] = 0
# vfs['e'][i,...,3] = pi/(w*h**3)* (ye*h**2-ye**3) * cos(pi*xe/w)

# 9
# vfs['u'][i,:,0] = sin(pi*xu/w) * sin(pi*yu/h)
# vfs['u'][i,:,1] = sin(pi*xu/w) * sin(pi*yu/h)
# vfs['e'][i,...,0] = pi/w * cos(pi*xe/w) * sin(pi*ye/h)
# vfs['e'][i,...,1] = pi/h * sin(pi*xe/w) * cos(pi*ye/h)
# vfs['e'][i,...,2] = pi/h * sin(pi*xe/w) * cos(pi*ye/h)
# vfs['e'][i,...,3] = pi/w * cos(pi*xe/w) * sin(pi*ye/h)


# 3D

# 1
# vfs['u'][i,:,0] = xu/w * (abs(yu)-h)/h
# vfs['u'][i,:,1] = 0
# vfs['u'][i,:,2] = 0
# vfs['e'][i,...,0] = (abs(ye)-h) / (w*h)
# vfs['e'][i,...,1] = 0
# vfs['e'][i,...,2] = 0
# vfs['e'][i,...,3] = sign(ye) * xe/(w*h)
# vfs['e'][i,...,4] = 0
# vfs['e'][i,...,5] = 0
# vfs['e'][i,...,6] = 0
# vfs['e'][i,...,7] = 0
# vfs['e'][i,...,8] = 0