import os
import numpy as np

import _funcs

def load_data(prjnm,tests,symm,nt):
    """
    Load coordinates, connectivity, and displacements.

    Parameters
    ----------
    prjname : str
        Name of current project.
    tests : object
        List of tests name.
    symm : (nt,(nsymm,)), int
        List of symmetry conditions.
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
    force : (nt,(nf,dof)) , float
        Global loading force.
    time : (nt,(nf,)) , float
        Time increments.
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
    time = [None]*nt
    centr = [None]*nt
    thick = np.zeros(nt)
    ori = np.zeros(nt)

    # Set project directory
    dir = f'input\{prjnm}'

    for t in range(nt):

        # Set test name
        tnm = tests[t]

        # Set test directory
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

        # Translate xyz origin to center of specimen
        lmin = np.nanmin(coord[t],0)
        lmax = np.nanmax(coord[t],0)

        # No symmetries
        if symm[t] is None:
            coord[t] = coord[t] - (lmin + lmax)/2
        else:
            # Symmetry condition in x-direction
            if (0 in symm[t]) and (1 not in symm[t]):
                coord[t,0] = coord[t,0] - lmin[0]
                coord[t,1] = coord[t,1] - (lmin[1] + lmax[1])/2

            # Symmetry condition in y-direction
            elif (0 not in symm[t]) and (1 in symm[t]):
                coord[t,0] = coord[t,0] - (lmin[0] + lmax[0])/2
                coord[t,1] = coord[t,1] - lmin[1]

            # Symmetry condition in x- and y-directions
            elif (0 in symm[t]) and (1 in symm[t]):
                coord[t] = coord[t] - lmin

        # Load elements connectivity
        filename = f'{filesdir}_Elements.csv'
        conn[t] = np.loadtxt(filename,int,skiprows=1,delimiter=';')[:,1:]

        # Load nodal displacements
        displ[t] = np.zeros((nf[t],coord[t].shape[0],coord[t].shape[1]))
        for f in range(nf[t]):
            filename = f'{filesdir}_U_{f}.csv'
            displ[t][f,:] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

        # Load global forces
        filename = f'{filesdir}_Force.csv'
        force[t] = np.loadtxt(filename,skiprows=1,delimiter=';')

        # Load time increments
        filename = f'{filesdir}_Time.csv'
        time[t] = np.loadtxt(filename,skiprows=1,delimiter=';')

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

    return coord,displ,conn,centr,force,time,thick,ori,nf