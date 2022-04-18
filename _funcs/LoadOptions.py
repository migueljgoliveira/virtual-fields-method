import re
import numpy as np

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
        _funcs.error('*Tests keyword is not defined in options file.')

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

def load_symmetry(data,ln,nt):
    """
    Load symmetry conditions.

    Parameters
    ----------
    data : (), str
        Options file data contents. 
    ln : int
        Line number of symmetry option in data file.
    nt : int
        Number of tests.

    Returns
    -------
    symm : (nt,(nsymm,)), int
        List of symmetry conditions.
    """

    symm = [None]*nt
    if ln != -1:
        for t in range(nt):
            symm[t] = np.array(data[ln+1+t].split(','),dtype=int) - 1

    return symm

def load_algorithm(data,ln):
    """
    Load name of optimization algorithm.

    Parameters
    ----------
    data : (), str
        Options file data contents. 
    ln : int
        Line number of optimization option in data file.

    Returns
    -------
    algo : str
        Name of optimization algorithm.
    """

    if ln != -1:
        algo = data[ln+1].lower()
    else:
        algo = 'lm'

    return algo

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

    ivfs = [None]*nt
    if ln != -1:
        for t in range(nt):
            ldata = data[ln+1+t].split(',')
            if int(ldata[0]) == t+1:

                # User-defined virtual fields
                if ldata[1].lower() == 'ud':
                    try:
                        lvfs = [int(i) for i in ldata[2:]]
                    except:
                        _funcs.error(f'{kw} Test {t+1} user-defined virtual fields uncorrectly defined.')

                    ivfs[t] = {'ud': lvfs}

                # Sensivitity-based virtual fields
                elif ldata[1].lower() == 'sb':
                    try:
                        dx = float(ldata[2])
                    except:
                        dx = 0.1

                    ivfs[t] = {'sb': {'dx': dx}}

                else:
                    _funcs.error(f'{kw} Test {t+1} type of virtual fields not available.')
            else:
                _funcs.error(f'{kw} Incorrect number for test {t+1}.')
    else:
        _funcs.error(f'{kw} Keyword is not defined in options file.')

    return ivfs

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
                        _funcs.error(f'{kw} {comp[i]} component not defined for test {t+1}.')

            else:
                _funcs.error(f'{kw} Keyword is required for test {t+1}.')

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
        _funcs.error('*Properties keyword is not defined in options file.')

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
            _funcs.error('*Variables keyword is not defined in options file.')

    nvars = np.sum(vars)

    if (run == 'identification') and (nvars == 0):
        _funcs.error('At least one identification variable should be defined.')

    return vars,nvars

def load_boundaries(data,ln,vars,algo,nprops):
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
    algo : str
        Name of optimization algorithm.
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

    # Check if identification variables have boundaries
    if algo == 'de':
        if np.isnan(bounds[vars]).any():
            _funcs.error("boundaries are not defined for identification variables.")

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
    filename = f'input\{prjnm}\{prjnm}.vfm'

    # Read settings file
    with open(filename,'r') as f:
        dataraw = f.readlines()

    # Clean settings data of comments and spaces
    data = []
    l = 0
    for line in dataraw:
        dataraw[l] = dataraw[l].strip('\n').replace(' ','')
        if not dataraw[l].startswith('**'):
            data.append(dataraw[l])
        l += 1

    # Get keywords line numbers
    lsim,lid,ltest,lfout,lnlgeom,lnsymm,lalgo,lvfs,lbc,lprops,lvars,lbounds,lconstr = [-1]*13
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
        elif '*nlgeom' in line:
            lnlgeom = l
        elif '*symmetry' in line:
            lnsymm = l
        elif '*algorithm' in line:
            lalgo = l
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
        _funcs.error('select only *Simulation or only *Identification option.')
    else:
        _funcs.error('select *Simulation or *Identification option.')

    # Load number and name of tests
    tests,nt = load_tests(data,ltest)

    # Load output folder name
    fout = load_output(data,lfout,prjnm)

    # Load flag for small or large (default) deformation framework
    nlgeom = load_nlgeom(data,lnlgeom)

    # Load symmetry conditions
    symm = load_symmetry(data,lnsymm,nt)

    # Load selected optimization algorithm
    algo = load_algorithm(data,lalgo)

    # Load selected virtual fields
    ivfs = load_virtual_fields(data,lvfs,nt)

    # Load output folder name
    bc = load_boundary_conditions(data,lbc,ivfs,nt)

    # Load material properties
    props,nprops = load_properties(data,lprops)

    # Load variables flags
    vars,nvars = load_variables(data,lvars,nprops,run)

    # Load identification properties boundaries
    bounds = load_boundaries(data,lbounds,vars,algo,nprops)

    # Load identification properties constraints
    constr = load_constraints(data,lconstr,nprops)

    return run,tests,fout,props,vars,bounds,constr,nlgeom,symm,algo,ivfs,bc,nprops,nvars,nt