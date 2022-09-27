import os
import re
import numpy as np

import _utils
import _funcs

def load_tests(data,ln):
    """
    Load number and name of tests.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of tests option in data file.
    prjnm : str
        Name of current project.

    Returns
    -------
    tests : (nt,) , str
        List of tests name.
    nt : int
        Number of tests.
    """

    if ln != -1:
        tests = []
        nt = int(data[ln+1])
        for i in range(nt):
            ldata = data[ln+2+i].split(',')
            tests.append(ldata[1])
    else:
        _utils.error('*Tests keyword is not defined in options file.')

    # Check if tests have unique names
    if len(list(set(tests))) != nt:
        _utils.error('Name of tests not unique (*Tests).')

    return tests,nt

def load_output(data,ln,prjnm):
    """
    Load output folder name.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of output option in data file.
    prjnm : str
        Name of current project.

    Returns
    -------
    fout : str
        Name of output folder.
    """

    if ln != -1:
        fout = data[ln+1]
    else:
        fout = prjnm

    return fout


def load_optimization(data,ln):
    """
    Load optimization settings.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of optimization option in data file.

    Returns
    -------
    fout : str
        Name of output folder.
    """
    kw = '*Optimization.'

    tol,maxiter = None,None

    if ln != -1:
        try:
            tol,maxiter = np.array(data[ln+1].split(','),dtype=float)
        except:
            if (tol is None) or (maxiter is None):
                _utils.error(f'{kw} Tolerance or maximum number of iterations is not defined.')
    else:
        tol = 1e-8
        maxiter = 500

    return tol,maxiter

def load_nlgeom(data,ln):
    """
    Load flag for small or large (default) deformation framework

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of nlgeom option in data file.

    Returns
    -------
    nlgeom : bool
        Flag for small or large deformation framework (0/1).
    """

    if ln != -1:
        nlgeom = bool(int(data[ln+1]))
    else:
        nlgeom = 1

    return nlgeom

def load_virtual_fields(data,ln,nt):
    """
    Load information on selected virtual fields.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of virtual fields option in data file.
    nt : int
        Number of tests.

    Returns
    -------
    ivfs : (nt,{'ud' or 'sb'}) , int
        List of selected virtual fields.
    """

    kw = '*Virtual Fields.'

    vfs = [None]*nt
    if ln != -1:
        for t in range(nt):
            ldata = data[ln+1+t].split(',')
            if int(ldata[0]) == t+1:

                # User-defined virtual fields
                if ldata[1].lower() == 'ud':
                    try:
                        lvfs = [int(i) for i in ldata[2:]]
                    except:
                        _utils.error(f'{kw} Test {t+1} user-defined virtual fields uncorrectly defined.')

                    vfs[t] = {'ud': lvfs}

                # Sensivitity-based virtual fields
                elif ldata[1].lower() == 'sb':
                    try:
                        dx = float(ldata[2])
                    except:
                        dx = 0.1

                    try:
                        scale = float(ldata[3])
                    except:
                        scale = 0.3

                    vfs[t] = {'sb': {'dx': dx, 'scale': scale}}

                else:
                    _utils.error(f'{kw} Test {t+1} type of virtual fields not available.')
            else:
                _utils.error(f'{kw} Incorrect number for test {t+1}.')
    else:
        _utils.error(f'{kw} Keyword is not defined in options file.')

    return vfs

def load_boundary_conditions(data,ln,ivfs,nt):
    """
    Load tests boundary conditions.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of boundary conditions option in data file.
    ivfs : (nt,{'ud' or 'sb'}) , int
        List of selected virtual fields.
    nt : int
        Number of tests.

    Returns
    -------
    bc : (nt,(2,4) or None) , int
        Tests boundary conditions.
    """

    kw = '*Boundary Conditions.'

    comp = ['X','Y','Z']

    bc = [None]*nt
    n = 0
    for t in range(nt):
        if list(ivfs[t].keys())[0] == 'sb':
            if ln != -1:
                bc[t] = np.zeros((2,4))
                for i in range(2):
                    ldata = data[ln+1+2*n+i].split(',')
                    try:
                        if int(ldata[0]) != t+1:
                            pass
                        else:
                            bc[t][i,:] = np.array([int(j) for j in ldata[1:]])
                    except:
                        _utils.error(f'{kw} {comp[i]} component not defined for test {t+1}.')

            else:
                _utils.error(f'{kw} Keyword is required for test {t+1}.')

            n += 1

    return bc

def load_properties(data,ln):
    """
    Load material properties

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of properties option in data file.

    Returns
    -------
    nprops : int
        Number of material properties.
    props : (nprops,) , float
        List of material properties.
    """

    if ln != -1:
        nprops = int(data[ln+1])

        props = np.zeros(nprops)
        for i in range(nprops):
            props[i] = float(data[ln+2+i].split(',')[-1])
    else:
        _utils.error('*Properties keyword is not defined in options file.')

    return props,nprops

def load_variables(data,ln,nprops,run):
    """
    Load identification variables flags.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of variables option in data file.

    Returns
    vars : (nprops,) , bool
        Flags for identification variables.
    nvars : int
        Number of identification variables.
    """

    vars = np.zeros(nprops,dtype=bool)
    if ln != -1:
        for i in range(nprops):
            vars[i] = bool(eval(data[ln+1+i].split(',')[-1]))
    else:
        if run == 'identification':
            _utils.error('*Variables keyword is not defined in options file.')

    nvars = np.sum(vars)

    if (run == 'identification') and (nvars == 0):
        _utils.error('At least one identification variable should be defined.')

    return vars,nvars

def load_boundaries(data,ln,vars,nprops):
    """
    Load identification variables boundaries.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of boundaries option in data file.
    vars : (nprops,) , bool
        Flags for identification variables.
    nprops : int
        Number of material properties.

    Returns
    -------
    bounds : (nprops,2) , float
        Boundaries for identification variables.
    """

    bounds = np.zeros((nprops,2)) * np.nan
    if ln != -1:
        try:
            nbound = int(data[ln+1])
            for i in range(nbound):
                idp = int(data[ln+2+i].split(',')[0]) - 1
                bounds[idp,0] = float(data[ln+2+i].split(',')[1])
                bounds[idp,1] = float(data[ln+2+i].split(',')[2])
        except:
            pass
    else:
        bounds[vars] = np.array([-np.inf,+np.inf])

    return bounds

def load_constraints(data,ln,nprops):
    """
    Load identification properties constraints.

    Parameters
    ----------
    data : (), str
        Options file data contents.
    ln : int
        Line number of constraints option in data file.
    nprops : int
        Number of material properties.

    Returns
    -------
    constr : (nprops,2) , float
        Constraints for identification properties.
    """

    constr = []
    if ln != -1:
        try:
            nconstr = int(data[ln+1])
            l = 0
            for line in data[ln+2:ln+2+nconstr]:
                idp = int(line.split(',')[0]) - 1
                expr = line.split(',')[1]
                for n in range(nprops):
                    expr = re.sub(f'\[{n+1}\]',f'props[{n}]',expr)
                constr.append([idp,expr])
                l += 1
        except:
            pass

    return constr

def load_options(prjnm):
    """
    Load options for virtual fields method.

    Parameters
    ----------
    prjnm : str
        Name of current project.

    Returns
    -------
    options : object
        Object with project options.
    """

    # Path to settings file
    filename = os.path.join(os.getcwd(),'input',prjnm,f'{prjnm}.vfm')

    # Read settings file
    try:
        with open(filename,'r') as f:
            dataraw = f.readlines()
    except:
        _utils.error('Project not found.')

    # Clean settings data of comments and spaces
    data = []
    l = 0
    for line in dataraw:
        dataraw[l] = dataraw[l].strip('\n').replace(' ','')
        if not dataraw[l].startswith('**'):
            data.append(dataraw[l])
        l += 1

    # Get keywords line numbers
    lsim = -1
    lid = -1
    ltest = -1
    lfout = -1
    lopti = -1
    lnlgeom = -1
    lvfs = -1
    lbc =-1 
    lprops = -1
    lvars = -1
    lbounds = -1
    lconstr = -1

    l = 0
    for line in data:
        line = line.lower()
        if '*simulation' in line:
            lsim = l
        elif '*identification' in line:
            lid = l
        elif '*tests' in line:
            ltest = l
        elif '*output' in line:
            lfout = l
        elif '*optimization' in line:
            lopti = l
        elif '*nlgeom' in line:
            lnlgeom = l
        elif '*virtualfields' in line:
            lvfs = l
        elif '*boundaryconditions' in line:
            lbc = l
        elif '*properties' in line:
            lprops = l
        elif '*variables' in line:
            lvars = l
        elif '*boundaries' in line:
            lbounds = l
        elif '*constraints' in line:
            lconstr = l

        l += 1

    # Set type of run
    if lsim != -1:
        run = 'simulation'
    elif lid != -1:
        run = 'identification'
    elif (lsim != -1) and (lid != -1):
        _utils.error('select only *Simulation or only *Identification option.')
    else:
        _utils.error('select *Simulation or *Identification option.')

    # Load number and name of tests
    tests,nt = load_tests(data,ltest)

    # Load output folder name
    fout = load_output(data,lfout,prjnm)

    # Load optimization seetings
    tol,maxiter = load_optimization(data,lopti)

    # Load flag for small or large (default) deformation framework
    nlgeom = load_nlgeom(data,lnlgeom)

    # Load selected virtual fields
    vfs = load_virtual_fields(data,lvfs,nt)

    # Load output folder name
    bc = load_boundary_conditions(data,lbc,vfs,nt)

    # Load material properties
    props,nprops = load_properties(data,lprops)

    # Load variables flags
    vars,nvars = load_variables(data,lvars,nprops,run)

    # Load identification properties boundaries
    bounds = load_boundaries(data,lbounds,vars,nprops)

    # Load identification properties constraints
    constr = load_constraints(data,lconstr,nprops)

    return run,tests,fout,tol,maxiter,props,vars,bounds,constr,nlgeom,vfs,bc,nprops,nvars,nt