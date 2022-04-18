import numpy as np

def nodes_connectivity(econn,nn,npe):

    nconn = -np.ones((nn,npe),dtype=int)

    for i in range(nn):
        idx = np.nonzero(econn == i)
        nconn[i,idx[1]] = idx[0]

    return nconn