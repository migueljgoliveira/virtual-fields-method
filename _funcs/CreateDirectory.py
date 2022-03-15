import os
import shutil

def create_directory(prjname,fout,tests,nt):
    """
    Create directory to export output files of current project.

    Parameters
    ----------
    prjname: str
        Name of current project.
    out : str
        Name of output folder.
    tests : (nt,) , str
        List of tests name.
    nt : int
        Number of tests.

    Returns
    -------
    dir : str
        Directory of project to export output files.
    """

    # Set directories
    cwd = os.getcwd()
    dirO = f'{cwd}\\output\\{fout}'

    # Delete old output folder
    if os.path.isdir(dirO):
        shutil.rmtree(dirO)

    # Create project output folder
    os.mkdir(dirO)

    # Create tests output folders
    if nt > 1:
        for t in range(nt):
            os.mkdir(f'{dirO}\{tests[t]}')

    # Copy options file to output folder
    dirI = f'{cwd}\input\{prjname}'
    shutil.copy2(f'{dirI}\{prjname}.vfm',f'{dirO}\{prjname}.vfm')