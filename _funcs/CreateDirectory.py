import os
import shutil

def create_directory(prjnm,fout,test,nt):
    """
    Create directory to export output files of current project.

    Parameters
    ----------
    prjnm: str
        Name of current project.
    fout : str
        Name of output folder.
    test : (nt,) , str
        List of tests name.
    nt : int
        Number of tests.

    Returns
    -------
    dirout : str
        Directory of project to export output files.
    """

    # Set directories
    outf = os.path.join(os.getcwd(),'output')
    dirout = os.path.join(outf,fout)

    # Create output folder
    if not os.path.isdir(outf):
        os.mkdir(outf)

    # Delete old output folder
    if os.path.isdir(dirout):
        shutil.rmtree(dirout)

    # Create project output folder
    os.mkdir(dirout)

    # Create tests output folders
    if nt > 1:
        for t in range(nt):
            os.mkdir(f'{dirout}\{test[t]}')

    # Copy options file to output folder
    dirin = os.path.join(os.getcwd(),'input',prjnm,f'{prjnm}.vfm')
    shutil.copy2(dirin,os.path.join(dirout,f'{prjnm}.vfm'))

    return dirout