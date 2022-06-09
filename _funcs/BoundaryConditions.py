import numpy as np

import _utils

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
    bcdofs : {'fixed','active','parent','child'} , int
        Boundary conditions degrees of freedom.

    Edges Nomeclature

         0000       Edge 0 --> max (1), y (1)
        3    1      Edge 2 --> min (0), y (1)
        3    1      Edge 1 --> max (1), x (0)
         2222       Edge 3 --> min (0), x (0)
    """

    kw = '*Boundary Conditions.'

    bcdofs = {'fixed': [],
              'active': [],
              'parent': [ [[],[]] , [[],[]] , [[],[]] , [[],[]] ],
              'child': [ [[],[]] , [[],[]] , [[],[]] , [[],[]] ]}

    # Coordinate flag ( 0 --> x and 1 --> y )
    cid = [1,0,1,0]

    # Limits flag ( 0 --> min and 1 --> max )
    lid = [1,1,0,0]

    # Minimum and maximum coordinates
    xlim = [np.min(coord[:,0]),np.max(coord[:,0])]
    ylim = [np.min(coord[:,1]),np.max(coord[:,1])]
    lims = [xlim,ylim]

    # Initialize counter for number of constant boundary conditions
    nconst = 0
    nfixed = 0

    for i in range(4):
        if (bc[:,i] != 0).any():

            # All nodes coordinate component
            cnodes = coord[:,cid[i]]

            # Edge boundary coordinate
            ledge = lims[cid[i]][lid[i]]

            # Nodes index in edge
            nodes = np.array(np.flatnonzero(cnodes == ledge),dtype=int)

            # Get corner node
            nmaster = nodes[np.argmax(coord[nodes,abs(cid[i]-1)])]
            nmaster = np.argmax(coord[nodes,abs(cid[i]-1)])

            # Loop over degrees of freedom
            const = np.zeros(2,dtype=bool)
            for j in range(2):

                # Fixed degree of freedom
                if bc[j,i] == 1:
                    bcdofs['fixed'].append(nodes*dof + j)

                    nfixed += 1

                # Constant degree of freedom
                elif bc[j,i] == 2:
                    bcdofs['child'][i][j] = np.delete(nodes*dof + j,nmaster)
                    bcdofs['parent'][i][j] = [nodes[nmaster]*dof + j]

                    nconst += 1
                    const[j] = True

            if const.all():
                _utils.error(f'{kw}. Constant boundary condition defined in both directions for edge {i+1} of test {t+1}')

    # Check if there is at least one constant boundary condition
    if nconst == 0:
        _utils.error(f'{kw}. At least one constant boundary condition should be defined for test {t+1}')

    # Check if exist fixed degrees of freedom and concatenate
    if nfixed != 0:
        bcdofs['fixed'] = np.hstack([i for i in bcdofs['fixed']])
    else:
        _utils.error(f'{kw} At least one fixed boundary condition should be defined for test {t+1}')

    # Check if exist constant degrees of freedom as child and add to fixed
    for i in range(4):
        for j in range(dof):
            bcdofs['fixed'] = np.append(bcdofs['fixed'],bcdofs['child'][i][j])

    bcdofs['fixed'] = np.array(bcdofs['fixed'],dtype=int)

    # Active degrees of freedom
    bcdofs['active'] = np.delete(np.arange(nn*dof),bcdofs['fixed'])

    return bcdofs