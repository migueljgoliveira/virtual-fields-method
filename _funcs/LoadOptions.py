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
        nlgeom : bool
            Flag for small or large deformation framework (0/1).
        algo : str
            Name of optimization algorithm.
        ivfs : (nt,{(nvfs)}) , int
            List of selected virtual fields.
        props : (nprops,) , float
            List of material properties.
        nprops : int
            Number of material properties. 
        opti : (nprops,) , bool
            Flags for identification properties.
        bounds : (nprops,2) , float
            Boundaries for identification properties.
        constr : (nprops,2) , float
            Constraints for identification properties.
        """

        self.tests = None
        self.fout = None
        self.nlgeom = None
        self.algo = None
        self.ivfs = None
        self.props = None
        self.nprops = None
        self.opti = None
        self.bounds = None
        self.constr = None

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
        """

        self.nlgeom = 1
        if ln != -1:
            self.nlgeom = bool(int(data[ln+1]))

    def load_algo(self,data,ln):
        """
        Load name of optimization algorithm.

        Parameters
        ----------
        data : (), str
            Options file data contents. 
        ln : int
            Line number of optimization option in data file.
        """

        if ln != -1:
            self.algo = data[ln+1].lower()

        # Default
        else:
            self.algo = 'lm'

    def load_vfs(self,data,ln,nt):
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

    def load_props(self,data,ln):
        """
        Load material properties

        Parameters
        ----------
        data : (), str
            Options file data contents. 
        ln : int
            Line number of properties option in data file.
        """

        self.nprops = int(data[ln+1])

        self.props = np.zeros(self.nprops)
        for i in range(self.nprops):
            self.props[i] = float(data[ln+2+i].split(',')[-1])

    def load_opti(self,data,ln):
        """
        Load identification properties flags

        Parameters
        ----------
        data : (), str
            Options file data contents. 
        ln : int
            Line number of identification option in data file.
        """

        self.opti = np.zeros(self.nprops,dtype=bool)
        for i in range(self.nprops):
            self.opti[i] = bool(eval(data[ln+1+i].split(',')[-1]))

    def load_bounds(self,data,ln):
        """
        Load identification properties boundaries.

        Parameters
        ----------
        data : (), str
            Options file data contents. 
        ln : int
            Line number of boundaries option in data file.
        """

        self.bounds = []
        if ln != -1:
            self.bounds = np.zeros((self.nprops,2)) * np.nan
            try:
                nbound = int(data[ln+1])
                for i in range(nbound):
                    idp = int(data[ln+2+i].split(',')[0])
                    self.bounds[idp,0] = float(data[ln+2+i].split(',')[1])
                    self.bounds[idp,1] = float(data[ln+2+i].split(',')[2])
            except:
                pass

    def load_constr(self,data,ln):
        """
        Load identification properties constraints.

        Parameters
        ----------
        data : (), str
            Options file data contents. 
        ln : int
            Line number of constraints option in data file.
        """

        self.constr = []
        if ln != -1:
            try:
                nconstr = int(data[ln+1])
                l = 0
                for line in data[ln+2:ln+2+nconstr]:
                    idp = int(line.split(',')[0])
                    expr = line.split(',')[1].replace('[','props[')
                    self.constr.append([idp,expr])
                    l += 1
            except:
                pass

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
    ltest,lfout,lnlgeom,lalgo,lvfs,lprops,lopti,lbounds,lconstr = [-1]*9
    l = 0
    for line in data:
        line = line.lower()
        if '*tests' in line:
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
        elif '*identification' in line:
            lopti = l
        elif '*boundaries' in line:
            lbounds = l
        elif '*constraints' in line:
            lconstr = l

        l += 1

    # Initialize options object
    options = Options()

    # Load number and name of tests
    nt = options.load_tests(data,ltest,prjnm)

    # Load output folder name
    options.load_output(data,lfout,prjnm)

    # Load flag for small or large (default) deformation framework
    options.load_nlgeom(data,lnlgeom)

    # Load selected optimization algorithm
    options.load_algo(data,lalgo)

    # Load selected virtual fields
    options.load_vfs(data,lvfs,nt)

    # Load material properties
    options.load_props(data,lprops)

    # Load identification properties flags
    options.load_opti(data,lopti)

    # Load identification properties boundaries
    options.load_bounds(data,lbounds)

    # Load identification properties constraints
    options.load_constr(data,lconstr)

    # Check if identification properties have boundaries
    if options.algo == 'de':
        if np.isnan(options.bounds[options.opti]).any():
            _funcs.Error("boundaries are not defined for identification properties.")

    return options,nt