import os
import shutil

def create_directory(prjname,fout,test,nt):
    """
    Create directory to export output files of current project.

    Parameters
    ----------
    prjname: str
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
    cwd = os.getcwd()
    outf = f'{cwd}\\output'
    dirout = f'{outf}\\{fout}'

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
    dirin = f'{cwd}\input\{prjname}'
    shutil.copy2(f'{dirin}\{prjname}.vfm',f'{dirout}\{prjname}.vfm')

    return dirout