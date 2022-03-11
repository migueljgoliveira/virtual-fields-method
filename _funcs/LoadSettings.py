import numpy as np

def load_settings(prjname):
    """
    Load settings for virtual fields method.

    Parameters
    ----------
    prjname : str
        Name of current project.

    Returns
    -------
    props : (nprops,) , float
        Material properties.
    opti : (nprops,) , bool
        Flags for identification properties.
    constr : (nprops,2) , float
        Constraints for identification properties.
    nprops : int
        Number of material properties. 
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    """

    # Path to settings file
    filename = f'input\{prjname}\{prjname}.vfm'

    # Read settings file and get keywords line numbers
    lprops,lopti,lbounds,lconstr,lnlgeom = -1,-1,-1,-1,-1
    with open(filename,'r') as f:
        data = f.readlines()
        l = 0
        for line in data:
            data[l] = line.strip('\n').replace(' ','')
            if '*Properties' in line:
                lprops = l
            if '*Identification' in line:
                lopti = l
            if '*Boundaries' in line:
                lbounds = l
            if '*Constraints' in line:
                lconstr = l
            if '*Nlgeom' in line:
                lnlgeom = l
            l += 1

    # Number of material properties
    nprops = int(data[lprops].replace(' ','').split(',')[-1][4:])

    # Load material properties
    props = np.loadtxt(filename,skiprows=lprops+1,max_rows=nprops,
                       usecols=1,delimiter=',')

    # Load identification properties flags
    opti = np.loadtxt(filename,dtype=bool,skiprows=lopti+1,max_rows=nprops,
                       usecols=1,delimiter=',')

    # Load identification properties boundaries
    bounds = np.loadtxt(filename,skiprows=lbounds+1,max_rows=nprops,
                        usecols=(1,2),delimiter=',')

    # Load identification properties constraints
    constr = []
    nconstr = int(data[lconstr].replace(' ','').split(',')[-1][4:])
    if lconstr != -1:
        l = 0
        for line in data[lconstr+1:lconstr+1+nconstr]:
            idprop = int(line.split(',')[0])
            expr = line.split(',')[1].replace('<','props[').replace('>',']')
            constr.append([idprop,expr])
            l += 1

    # Set flag for small or large (default) deformation framework
    nlgeom = 1
    if lnlgeom != -1:
        nlgeom = bool(int(data[lnlgeom+1]))

    return props,opti,bounds,constr,nprops,nlgeom