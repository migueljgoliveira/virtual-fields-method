import numpy as np

import _funcs
def boundary_conditions(coord,nn,dof,bc,t):
    """
    Get nodes degrees of freedom according to their status.

    Parameters
    ----------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    nn : int
        Number of nodes.
    dof : int
        Number of degrees of freedom.
    bc : (dof,4) , int
        Test boundary conditions.
    t : int
        Test number.

    Returns
    -------
    bccte : (4,()) , int
        Contant degrees of freedom per edge.
    bcfix : (nbcfix) , int
        Fixed degrees of freedom.
    bcact : (nbcact) , int
        Active degrees of freedom.

    Notes
    -----
    nbcfix : int
        Number of fixed degrees of freedom.
    nbcact : int
        Number of active degrees of freedom.

    Edges Nomeclature

         00000        Edge 0 --> max (1), y (1)
        3     1       Edge 2 --> min (0), y (1)
        3     1       Edge 1 --> max (1), x (0)
         22222        Edge 3 --> min (0), x (0)

    """

    kw = '*Boundary Conditions.'

    bcfix = []
    bcact = []
    bccte = [ [[],[]] , [[],[]] , [[],[]] , [[],[]] ]

    # Coordinate flag ( 0 --> x and 1 --> y )
    cid = [1,0,1,0]

    # Limits flag ( 0 --> min and 1 --> max )
    lid = [1,1,0,0]

    # Minimum and maximum coordinates
    xlim = [np.min(coord[:,0]),np.max(coord[:,0])]
    ylim = [np.min(coord[:,1]),np.max(coord[:,1])]
    lims = [xlim,ylim]

    for i in range(4):
        if (bc[:,i] != 0).any():

            # All nodes coordinate component
            cnodes = coord[:,cid[i]]

            # Edge boundary coordinate
            ledge = lims[cid[i]][lid[i]]

            # Nodes index in edge
            nodes = np.array(np.flatnonzero(cnodes == ledge),dtype=int)

            # Loop over degrees of freedom
            for j in range(2):

                # Fixed degree of freedom
                if bc[j,i] == 1:
                    bcfix.append(nodes*dof + j)

                # Constant degree of freedom
                elif bc[j,i] == 2:
                    bccte[i][j] = nodes*dof + j

            if (len(bccte[i][0]) > 1) and (len(bccte[i][1]) > 1):
                _funcs.error(f'{kw}. Constant boundary condition defined in both directions for edge {i+1} of test {t+1}')

    # Check if there is at least one constant boundary condition
    for i in range(4):
        if (len(bccte[i][0]) < 1) and (len(bccte[i][1]) < 1):
            _funcs.error(f'{kw}. At least one constant boundary condition should be defined for test {t+1}')
        else:
            break

    # Check if exist fixed degrees of freedom and concatenate
    if len(bcfix) > 0:
        bcfix = np.array(np.concatenate(([i for i in bcfix])),dtype=int)
    else:
        _funcs.error(f'{kw} At least one fixed boundary condition should be defined for test {t+1}')

    # Active degrees of freedom
    bcact = np.delete(np.arange(nn*dof),bcfix)

    return bccte,bcfix,bcact