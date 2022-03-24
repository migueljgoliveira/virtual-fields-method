import os
import numpy as np

import _funcs

def load_data(prjnm,tests,nt):
    """
    Load coordinates, connectivity, and displacements.

    Parameters
    ----------
    prjname : str
        Name of current project.
    tests : object
        OList of tests name.
    nt : int
        Number of tests.

    Returns
    -------
    coord : (nt,(nn,dof)) , float
        Nodes reference coordinates.
    displ : (nt,(nf,nn,dof)) , float
        Nodes displacements.
    conn : (nt,(ne,npe)) , int
        Elements connectivity.
    centroid : (nt,(ne,dof)) , float
        Elements centroid reference coordinates.
    force : (nt,(nf,dof)),float
        Global loading force.
    thick : (nt,) , float
        Specimen initial thickness.
    ori : (nt,) , float
        Material orientation angle in degrees.
    nf : (nt,) , int
        Number of increments.
    """

    # Initialize data variables
    nf = np.zeros(nt,dtype=int)
    coord = [None]*nt
    conn = [None]*nt
    displ = [None]*nt
    force = [None]*nt
    centr = [None]*nt
    thick = np.zeros(nt)
    ori = np.zeros(nt)

    # Set project directory
    dir = f'input\{prjnm}'

    for t in range(nt):

        # Set test name
        tnm = tests[t]

        # Set test directory
        if nt == 1:
            basedir = f'{dir}'
            filesdir = f'{dir}\{tnm}'
        else:
            basedir = f'{dir}\{tnm}'
            filesdir = f'{dir}\{tnm}\{tnm}'

        # Get number of increments
        files = os.listdir(basedir)
        for file in files:
            try:
                if file.split('_')[-2] == 'U':
                    nf[t] = nf[t] + 1
            except:
                pass

        # Load nodal coordinates
        filename = f'{filesdir}_Nodes.csv'
        coord[t] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

        # Load elements connectivity
        filename = f'{filesdir}_Elements.csv'
        conn[t] = np.loadtxt(filename,int,skiprows=1,delimiter=';')[:,1:]

        # Load nodal displacements
        displ[t] = np.zeros((nf[t],coord[t].shape[0],coord[t].shape[1]))
        for f in range(nf[t]):
            filename = f'{filesdir}_U_{f}.csv'
            displ[t][f,:] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

        # Load global forcesq
        filename = f'{filesdir}_Force.csv'
        force[t] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

        # Check if force increments is equal to displacement increments
        if len(force[t]) != nf[t]:
            _funcs.error(f'number of force increments is different from displacement increments in test {t+1}.')

        # Load specimen thickness
        filename = f'{filesdir}_Thickness.csv'
        thick[t] = float(np.loadtxt(filename,skiprows=1,delimiter=';'))

        # Load material orientation
        filename = f'{filesdir}_Orientation.csv'
        ori[t] = 90 - float(np.loadtxt(filename,skiprows=1,delimiter=';'))

        # Compute elements centroid
        centr[t] = np.mean(coord[t][conn[t]],1)

    return coord,displ,conn,centr,force,thick,ori,nf