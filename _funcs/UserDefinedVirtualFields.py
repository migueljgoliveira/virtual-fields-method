import numpy as np
from numpy import pi,sin,cos,sign

def user_defined_virtual_fields(coord,centr,ne,dof,vfs):
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
    xu,yu = np.max(xn),np.max(yn)

    # Create variables to store virtual fields
    vfs['e'] = np.zeros((nvfs,1,ne,dof*dof))
    vfs['u'] = np.zeros((nvfs,1,dof))

    # Generate user-defined virtual fields - 2D
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
                vfs['u'][i,:,0] = xu / w
                vfs['u'][i,:,1] = 0

                vfs['e'][i,...,0] = 1 / w
                vfs['e'][i,...,1] = 0

                vfs['e'][i,...,2] = 0
                vfs['e'][i,...,3] = 0

            # Type 3
            if ivf == 3:
                vfs['u'][i,:,0] = xu/w * (abs(yu)-h)/h
                vfs['u'][i,:,1] = 0

                vfs['e'][i,...,0] = (abs(ye)-h) / (w*h)
                vfs['e'][i,...,1] = 0

                vfs['e'][i,...,2] = sign(ye) * xe/(w*h)
                vfs['e'][i,...,3] = 0

            # Type 4
            if ivf == 4:
                vfs['u'][i,:,0] = 1/pi * sin(pi*xu/w) * cos(pi*yu/(2*h))
                vfs['u'][i,:,1] = 1/pi * sin(pi*xu/w) * cos(pi*yu/(2*h))

                vfs['e'][i,...,0] = 1/w * cos(pi*xe/w) * cos(pi*ye/(2*h))
                vfs['e'][i,...,1] = -1/(2*h) * sin(pi*xe/w) * sin(pi*ye/(2*h))

                vfs['e'][i,...,2] = -1/(2*h) * sin(pi*xe/w) * sin(pi*ye/(2*h))
                vfs['e'][i,...,3] = 1/w * cos(pi*xe/w) * cos(pi*ye/(2*h))

            # Type 5
            if ivf == 5:
                vfs['u'][i,:,0] = xu*(yu**2-yu*h) / (w*h**2)
                vfs['u'][i,:,1] = 0

                vfs['e'][i,...,0] = (ye**2-ye*h) / (w*h**2)
                vfs['e'][i,...,1] = 0

                vfs['e'][i,...,2] = xe*(2*ye-h) / (w*h**2)
                vfs['e'][i,...,3] = 0

            # Type 6
            if ivf == 6:
                vfs['u'][i,:,0] = sin(pi*xu/w) * sin(pi*yu/h)
                vfs['u'][i,:,1] = 0

                vfs['e'][i,...,0] = pi/w * cos(pi*xe/w) * sin(pi*ye/h)
                vfs['e'][i,...,1] = 0

                vfs['e'][i,...,2] = pi/h * sin(pi*xe/w) * cos(pi*ye/h)
                vfs['e'][i,...,3] = 0

            # Type 7
            if ivf == 7:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = sin(pi*xu/w) * sin(pi*yu/h)

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = pi/h * sin(pi*xe/w) * cos(pi*ye/h)

                vfs['e'][i,...,2] = 0
                vfs['e'][i,...,3] = pi/w * cos(pi*xe/w) * sin(pi*ye/h)

            # Type 8
            if ivf == 8:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = xu*(yu**2-yu*h) / (w*h**2)

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = xe*(2*ye-h) / (w*h**2)

                vfs['e'][i,...,2] = 0
                vfs['e'][i,...,3] = (ye**2-ye*h) / (w*h**2)

            # Type 9
            if ivf == 9:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = (yu**2*h-yu**3)/h**3 * sin(pi*xu/w)

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = (2*h*ye-3*ye**2)/h**3 * sin(pi*xe/w)

                vfs['e'][i,...,2] = 0
                vfs['e'][i,...,3] = pi/(w*h**3)* (h*ye**2-ye**3) * cos(pi*xe/w)

            # Type 10
            if ivf == 10:
                vfs['u'][i,:,0] = ((h**3-yu**3)/h**3) * sin(pi*xu/w)
                vfs['u'][i,:,1] = 0

                vfs['e'][i,...,0] = pi*(h**3-ye**3)/(w*h**3) * cos(pi*xe/w)
                vfs['e'][i,...,1] = 0

                vfs['e'][i,...,2] = - ((3*ye**2)/h**3) * sin(pi*xe/w)
                vfs['e'][i,...,3] = 0

            # Type 11
            if ivf == 11:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = (yu*h**2-yu**3)/h**3 * sin(pi*xu/w)

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = (h**2-3*ye**2)/h**3 * sin(pi*xe/w)

                vfs['e'][i,...,2] = 0
                vfs['e'][i,...,3] = pi/(w*h**3)* (ye*h**2-ye**3) * cos(pi*xe/w)

            i += 1

    # Generate user-defined virtual fields - 3D
    if dof == 3:
        i = 0
        for ivf in vfs['ud']:

            # Type 1
            if ivf == 1:
                vfs['u'][i,:,0] = 0
                vfs['u'][i,:,1] = yu / h
                vfs['u'][i,:,2] = 0

                vfs['e'][i,...,0] = 0
                vfs['e'][i,...,1] = 1 / h
                vfs['e'][i,...,2] = 0

                vfs['e'][i,...,3] = 0
                vfs['e'][i,...,4] = 0

                vfs['e'][i,...,5] = 0
                vfs['e'][i,...,6] = 0

                vfs['e'][i,...,7] = 0
                vfs['e'][i,...,8] = 0

            i += 1

    return vfs,nvfs