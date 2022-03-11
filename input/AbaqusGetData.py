from odbAccess import *
from abaqusConstants import *

import numpy as np
from textRepr import prettyPrint as pp

def main():

    # input settings
    dof = 2
    folder = 'Double-Notched-2D'
    odbFile = folder

    # nodes per element
    if dof == 2:
        npe = 4
        ntens = 3
    elif dof == 3:
        npe = 8
        ntens = 6

    # open odb file
    odb = openOdb('%s/%s.odb'%(folder,odbFile),readOnly=1)

    nset = odb.rootAssembly.nodeSets['ROI']
    elset = odb.rootAssembly.elementSets['ROI']

    # get reference coordinates
    nn = len(nset.nodes[0])
    coord = np.zeros((nn,dof+1))
    for i in range(nn):
        coord[i,0] = nset.nodes[0][i].label - 1
        coord[i,1:] = nset.nodes[0][i].coordinates[:dof]

    # get elements connectivity
    ne = len(elset.elements[0])
    conn = np.zeros((ne,npe+1))
    for i in range(ne):
        conn[i,0] = elset.elements[0][i].label - 1
        conn[i,1:] = np.array(elset.elements[0][i].connectivity) - 1

    # number of increments
    nf = len(odb.steps['Step-1'].frames)

    # get nodes displacements
    displ = np.zeros((nf,nn,dof+1))
    for i in range(nf):
        fieldOut = odb.steps['Step-1'].frames[i].fieldOutputs

        auxdispl = fieldOut['U'].getSubset(region=nset,position=NODAL)
        displ[i,:,0] = auxdispl.bulkDataBlocks[0].nodeLabels  - 1
        displ[i,:,1:] = auxdispl.bulkDataBlocks[0].data

    # get load force
    lset = odb.rootAssembly.nodeSets['TOP_EDGE']
    force = np.zeros((nf,dof+1))
    for i in range(nf):
        fieldOut = odb.steps['Step-1'].frames[i].fieldOutputs
        auxforce = fieldOut['RF'].getSubset(region=lset,position=NODAL)
        force[i,0] = odb.steps['Step-1'].frames[i].frameValue
        force[i,2] = abs(np.sum(auxforce.bulkDataBlocks[0].data[:,1]))

    # normalise nodes and elements numbering
    newconn = np.zeros_like(conn)
    nid = np.arange(0,nn)
    for i in range(ne):

        newconn[i,0] = i
        j = 1
        for n in conn[i,1:]:
            newconn[i,j] = nid[np.where(n == coord[:,0])[0][0]]
            j += 1

    coord[:,0] = nid
    displ[:,:,0] = nid

    with open('%s/%s_Elements.csv'%(folder,odbFile),'w') as f:
        if npe == 4:
            f.write('Element;Node-1;Node-2;Node-3;Node-4\n')
        if npe == 8:
            f.write('Element;Node-1;Node-2;Node-3;Node-4;Node-5;Node-6;Node-7;Node-8\n')
        np.savetxt(f,newconn,fmt='%d',delimiter=';')

    with open('%s/%s_Nodes.csv'%(folder,odbFile),'w') as f:
        if dof == 2:
            f.write('Node;X;Y\n')
        if dof == 3:
            f.write('Node;X;Y;Z\n')
        np.savetxt(f,coord,fmt='%.12f',delimiter=';')

    for i in range(nf):
        with open('%s/%s_U_%d.csv'%(folder,odbFile,i),'w') as f:
            if dof == 2:
                f.write('Node;U;V\n')
            if dof == 3:
                f.write('Node;U;V;W\n')
            np.savetxt(f,displ[i,...],fmt='%.12f',delimiter=';')

    with open('%s/%s_Force.csv'%(folder,odbFile),'w') as f:
        if dof == 2:
            f.write('Time;X;Y\n')
        if dof == 3:
            f.write('Time;X;Y;Z\n')
        np.savetxt(f,force,fmt='%.12f',delimiter=';')

    return

if __name__ == "__main__":

    # call main function
    main()