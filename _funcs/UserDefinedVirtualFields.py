import numpy as np
from numpy import pi,sin,cos,sign

def user_defined_virtual_fields(coord,centr,ne,dof,ivfs):
    """
    Generate user defined virtual fields.

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
        List of user defined virtual fields type. 

    Returns
    -------
    vfs : {(nvfs,ne,dof,dof), (nvfs,nn,dof)} , float
        User defined virtual fields.
    nvfs : int
        Number of virtual fields.

    Notes
    -----
    nn : int
        Number of nodes.
    """

    # Number of user defined virtual fields
    nvfs = len(ivfs['ud'])

    # Compute half-width and half-height of geometry
    w,h = abs(np.max(coord,0) - np.min(coord,0))/2

    # Create nodes coordinate and elements centroid variables
    xn,yn = coord[:,0],coord[:,1]
    xe,ye = centr[:,0],centr[:,1]

    # Compute maximum edge boundary coordinates
    xb,yb = np.max(xn),np.max(yn)

    # Create variable to store virtual fields
    vfs = {'e': np.zeros((nvfs,ne,dof,dof)),
           'u': np.zeros((nvfs,dof))}

    i = 0
    for ivf in ivfs['ud']:

        # Type 1
        if ivf == 1:
            vfs['u'][i,0] = 0
            vfs['u'][i,1] = yb / h

            vfs['e'][i,:,0,0] = 0
            vfs['e'][i,:,1,1] = 1 / h
            vfs['e'][i,:,0,1] = 0
            vfs['e'][i,:,1,0] = 0

        # Type 2
        if ivf == 2:
            vfs['u'][i,0] = xb / w
            vfs['u'][i,1] = 0

            vfs['e'][i,:,0,0] = 1 / w
            vfs['e'][i,:,1,1] = 0
            vfs['e'][i,:,0,1] = 0
            vfs['e'][i,:,1,0] = 0

        # Type 3
        if ivf == 3:
            vfs['u'][i,0] = (xb/w) * (abs(yb)-h)/h
            vfs['u'][i,1] = 0.0

            vfs['e'][i,:,0,0] = (abs(ye)-h) / (w*h)
            vfs['e'][i,:,1,1] = 0
            vfs['e'][i,:,0,1] = sign(ye) * xe/(w*h)
            vfs['e'][i,:,1,0] = 0

        # Type 4
        if ivf == 4:
            vfs['u'][i,0] = (1/pi) * sin(pi*xb/w) * cos(pi*yb/(2*h))
            vfs['u'][i,1] = (1/pi) * sin(pi*xb/w) * cos(pi*yb/(2*h))

            vfs['e'][i,:,0,0] = (1/w) * cos(pi*xe/w) * cos(pi*ye/(2*h))
            vfs['e'][i,:,1,1] = -(1/(2*h)) * sin(pi*xe/w) * sin(pi*ye/(2*h))
            vfs['e'][i,:,0,1] = -(1/(2*h)) * sin(pi*xe/w) * sin(pi*ye/(2*h))
            vfs['e'][i,:,1,0] = (1/w) * cos(pi*xe/w) * cos(pi*ye/(2*h))

        # Type 5
        if ivf == 5:
            vfs['u'][i,0] = ((xb*(yb**2-yb*h))/(w*h**2))
            vfs['u'][i,1] = 0

            vfs['e'][i,:,0,0] = (ye**2-ye*h)/(w*ye**2)
            vfs['e'][i,:,1,1] = 0
            vfs['e'][i,:,0,1] = (2*(xe*ye-1)/(w*h**2))
            vfs['e'][i,:,1,0] = 0

        i += 1

    return vfs,nvfs