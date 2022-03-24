import numpy as np

import _funcs

class Options:

    def __init__(self):
        """
        Variables
        -------
        tests : (nt,) , str
            List of tests name.
        fout : str
            Name of output folder.
        ivfs : (nt,{(nvfs)}) , int
            List of selected virtual fields.
        """

        self.tests = None
        self.fout = None
        self.ivfs = None

    def load_tests(self,data,ln,prjnm):
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
        nt : int
            Number of tests.
        """

        nt = 1
        self.tests = []
        if ln != -1:
            nt = int(data[ln+1])
            for i in range(1,nt+1):
                self.tests.append(data[ln+1+i])
        else:
            self.tests.append(prjnm)

        return nt

    def load_output(self,data,ln,prjnm):
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
        """

        self.fout = prjnm
        if ln != -1:
            self.fout = data[ln+1]

    def load_nlgeom(self,data,ln):
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

        nlgeom = 1
        if ln != -1:
            nlgeom = bool(int(data[ln+1]))

        return nlgeom

    def load_algorithm(self,data,ln):
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

        # Default
        else:
            algo = 'lm'

        return algo

    def load_virtualfields(self,data,ln,nt):
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
        """

        self.ivfs = [None]*nt
        if ln != -1:
            if data[ln+1].lower() == 'ud':
                for t in range(nt):
                    lvfs = [int(i) for i in data[ln+2+t].split(',')]
                    self.ivfs[t] = {'ud': lvfs}

        # Default
        else:
            self.ivfs = {'ud': [[1,3,4]]*self.nt}

    def load_properties(self,data,ln):
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

        nprops = int(data[ln+1])

        props = np.zeros(nprops)
        for i in range(nprops):
            props[i] = float(data[ln+2+i].split(',')[-1])

        return props,nprops

    def load_variables(self,data,ln,nprops):
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
        for i in range(nprops):
            vars[i] = bool(eval(data[ln+1+i].split(',')[-1]))

        nvars = np.sum(vars)

        return vars,nvars

    def load_boundaries(self,data,ln,vars,algo,nprops):
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
                    idp = int(data[ln+2+i].split(',')[0])
                    bounds[idp,0] = float(data[ln+2+i].split(',')[1])
                    bounds[idp,1] = float(data[ln+2+i].split(',')[2])
            except:
                pass

        # Check if identification variables have boundaries
        if algo == 'de':
            if np.isnan(bounds[vars]).any():
                _funcs.error("boundaries are not defined for identification variables.")

        return bounds

    def load_constraints(self,data,ln):
        """
        Load identification properties constraints.

        Parameters
        ----------
        data : (), str
            Options file data contents. 
        ln : int
            Line number of constraints option in data file.

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
                    idp = int(line.split(',')[0])
                    expr = line.split(',')[1].replace('[','props[')
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
    lsim,lid,ltest,lfout,lnlgeom,lalgo,lvfs,lprops,lvars,lbounds,lconstr = [-1]*11
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
        elif '*algorithm' in line:
            lalgo = l
        elif '*virtualfields' in line:
            lvfs = l
        elif '*properties' in line:
            lprops = l
        elif '*variables' in line:
            lvars = l
        elif '*boundaries' in line:
            lbounds = l
        elif '*constraints' in line:
            lconstr = l

        l += 1

    # Initialize options object
    options = Options()

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
    nt = options.load_tests(data,ltest,prjnm)

    # Load output folder name
    options.load_output(data,lfout,prjnm)

    # Load flag for small or large (default) deformation framework
    nlgeom = options.load_nlgeom(data,lnlgeom)

    # Load selected optimization algorithm
    algo = options.load_algorithm(data,lalgo)

    # Load selected virtual fields
    options.load_virtualfields(data,lvfs,nt)

    # Load material properties
    props,nprops = options.load_properties(data,lprops)

    # Load variables flags
    vars,nvars = options.load_variables(data,lvars,nprops)

    # Load identification properties boundaries
    bounds = options.load_boundaries(data,lbounds,vars,algo,nprops)

    # Load identification properties constraints
    constr = options.load_constraints(data,lconstr)

    return run,props,vars,bounds,constr,nlgeom,algo,nprops,nvars,nt,options