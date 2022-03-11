import os
import numpy as np

def load_data(name):
    """
    Load coordinates, connectivity, and displacements.

    Parameters
    ----------
    name : str
        Name of current project.

    Returns
    -------
    coord : (nn,dof) , float
        Nodes reference coordinates.
    displ : (nf,nn,dof) , float
        Nodes displacements.
    conn : (ne,npe) , int
        Elements connectivity.
    centroid : (ne,dof) , float
        Elements centroid reference coordinates.
    force : (nf,dof),float
        Global loading force.
    thick : float
        Specimen initial thickness.
    ori : float
        Material orientation angle in degrees.
    nf : int
        Number of increments.
    """

    # Set directories
    dir = f'input\{name}'
    basedir = f'{dir}\{name}'

    # Get number of increments
    files = os.listdir(dir)
    nf = 0
    for file in files:
        try:
            if file.split('_')[-2] == 'U':
                nf = nf + 1
        except:
            pass

    # Load nodal coordinates
    filename = f'{basedir}_Nodes.csv'
    coord = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

    # Load elements connectivity
    filename = f'{basedir}_Elements.csv'
    conn = np.loadtxt(filename,int,skiprows=1,delimiter=';')[:,1:]

    # Load nodal displacements
    displ = np.zeros((nf,coord.shape[0],coord.shape[1]))
    for i in range(nf):
        filename = f'{basedir}_U_{i}.csv'
        displ[i,:] = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

    # Load global force
    filename = f'{basedir}_Force.csv'
    force = np.loadtxt(filename,skiprows=1,delimiter=';')[:,1:]

    # Load specimen thickness
    filename = f'{basedir}_Thickness.csv'
    thick = float(np.loadtxt(filename,skiprows=1,delimiter=';'))

    # Load material orientation
    filename = f'{basedir}_Orientation.csv'
    ori = float(np.loadtxt(filename,skiprows=1,delimiter=';'))

    # Compute elements centroid
    centroid = np.mean(coord[conn],1)

    return coord,displ,conn,centroid,force,thick,ori,nf