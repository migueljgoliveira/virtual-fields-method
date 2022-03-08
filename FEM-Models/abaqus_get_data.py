from odbAccess import *
from abaqusConstants import *

import numpy as np
from textRepr import prettyPrint as pp

def main():

    # input settings
    dof = 2
    odbFile = '9elem-distload-elastic'
    output = '9elem-distload-elastic'

    # nodes per element
    if dof == 2:
        npe = 4
    elif dof == 3:
        npe = 8

    # open odb file
    odb = openOdb('%s.odb'%(odbFile),readOnly=1)

    # get reference coordinates
    nset = odb.rootAssembly.nodeSets[' ALL NODES']
    nn = len(nset.nodes[0])
    coord = np.zeros((nn,dof+1))
    for i in range(nn):
        coord[i,0] = nset.nodes[0][i].label - 1
        coord[i,1:] = nset.nodes[0][i].coordinates[:dof]

    # get elements connectivity
    elset = odb.rootAssembly.elementSets[' ALL ELEMENTS']
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
    lset = odb.rootAssembly.nodeSets['LOAD']
    force = np.zeros((nf,dof+1))
    for i in range(nf):
        fieldOut = odb.steps['Step-1'].frames[i].fieldOutputs
        auxforce = fieldOut['RF'].getSubset(region=lset,position=NODAL)
        force[i,0] = odb.steps['Step-1'].frames[i].frameValue
        force[i,2] = abs(np.sum(auxforce.bulkDataBlocks[0].data[:,1]))

    with open('%s_Elements.csv'%(output),'w') as f:
        if npe == 4:
            f.write('Element;Node-1;Node-2;Node-3;Node-4\n')
        if npe == 8:
            f.write('Element;Node-1;Node-2;Node-3;Node-4;Node-5;Node-6;Node-7;Node-8\n')
        np.savetxt(f,conn,fmt='%d',delimiter=';')

    with open('%s_Nodes.csv'%(output),'w') as f:
        if dof == 2:
            f.write('Node;X;Y\n')
        if dof == 3:
            f.write('Node;X;Y;Z\n')
        np.savetxt(f,coord,fmt='%.12f',delimiter=';')

    for i in range(nf):
        with open('%s_U_%d.csv'%(output,i),'w') as f:
            if dof == 2:
                f.write('Node;U;V\n')
            if dof == 3:
                f.write('Node;U;V;W\n')
            np.savetxt(f,displ[i,...],fmt='%.12f',delimiter=';')

    with open('%s_Force.csv'%(output),'w') as f:
        if dof == 2:
            f.write('Time;X;Y\n')
        if dof == 3:
            f.write('Time;X;Y;Z\n')
        np.savetxt(f,force,fmt='%.12f',delimiter=';')


    # get stress
    stress = np.zeros((nf,ne,3+1))
    for i in range(nf):
        fieldOut = odb.steps['Step-1'].frames[i].fieldOutputs

        auxstress = fieldOut['S'].getSubset(region=elset,position=CENTROID)
        stress[i,:,0] = auxstress.bulkDataBlocks[0].elementLabels  - 1
        stress[i,:,1:] = auxstress.bulkDataBlocks[0].data[:,[0,1,3]]

    for i in range(nf):
        with open('%s_S_%d.csv'%(output,i),'w') as f:
            if dof == 2:
                f.write('Element;XX;YY;XY\n')
            if dof == 3:
                f.write('Element;XX;YY;ZZ;XY;XZ;YZ\n')
            np.savetxt(f,stress[i,...],fmt='%.12f',delimiter=';')
    return

if __name__ == "__main__":

    # call main function
    main()