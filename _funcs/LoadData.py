import os
import numpy as np

import _funcs

def load_data(prjnm,test,nt):
    """
    Load coordinates, connectivity, and displacements.

    Parameters
    ----------
    prjname : str
        Name of current project.
    test : object
        List of tests name.
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
    thk : (nt,) , float
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
    thk = np.zeros(nt)
    ori = np.zeros(nt)

    # Set project directory
    dir = os.path.join('input',prjnm)

    for t in range(nt):

        # Set test name
        tnm = test[t]

        # Set files test directory
        filesdir = os.path.join(dir,tnm,tnm)

        # Load time increments
        filename = f'{filesdir}_Time.csv'
        time[t] = np.loadtxt(filename,skiprows=1,delimiter=';')

        # Get number of time increments
        nf[t] = len(time[t])

        # Load global forces
        filename = f'{filesdir}_Force.csv'
        force[t] = np.loadtxt(filename,skiprows=1,delimiter=';')

        # Check if force increments is equal to time increments
        if len(force[t]) != nf[t]:
            _funcs.error(f'number of force increments is different from time increments in test {t+1}.')

        # Load nodal coordinates
        filename = f'{filesdir}_Nodes.csv'
        coord[t] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

        # Translate xyz origin to center of specimen
        lmin = np.nanmin(coord[t],0)
        lmax = np.nanmax(coord[t],0)
        coord[t] = coord[t] - (lmin + lmax)/2

        # Load elements connectivity
        filename = f'{filesdir}_Elements.csv'
        conn[t] = np.loadtxt(filename,int,skiprows=1,delimiter=';')[:,1:]

        # Load nodal displacements
        displ[t] = np.zeros((nf[t],coord[t].shape[0],coord[t].shape[1]))
        for f in range(nf[t]):
            filename = f'{filesdir}_U_{f}.csv'
            displ[t][f] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

        # Load specimen thickness
        filename = f'{filesdir}_Thickness.csv'
        thk[t] = float(np.loadtxt(filename,skiprows=1,delimiter=';'))

        # Load material orientation
        filename = f'{filesdir}_Orientation.csv'
        ori[t] = 90 - float(np.loadtxt(filename,skiprows=1,delimiter=';'))

        # Compute elements centroid
        centr[t] = np.mean(coord[t][conn[t]],1)

    return coord,displ,conn,centr,force,time,thk,ori,nf