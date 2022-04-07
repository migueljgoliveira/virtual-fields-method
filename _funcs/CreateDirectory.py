import os
import shutil

def create_directory(prjname,fout,tests,nt):
    """
    Create directory to export output files of current project.

    Parameters
    ----------
    prjname: str
        Name of current project.
    fout : str
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
    dirout = f'{cwd}\\output\\{fout}'

    # Delete old output folder
    if os.path.isdir(dirout):
        shutil.rmtree(dirout)

    # Create project output folder
    os.mkdir(dirout)

    # Create tests output folders
    if nt > 1:
        for t in range(nt):
            os.mkdir(f'{dirout}\{tests[t]}')

    # Copy options file to output folder
    dirin = f'{cwd}\input\{prjname}'
    shutil.copy2(f'{dirin}\{prjname}.vfm',f'{dirout}\{prjname}.vfm')

    # Create log file
    with open(f'{dirout}\{fout}.log','w') as f:
        head = f'\n{" "*7}~~~~~~ VIRTUAL FIELDS METHOD ~~~~~~\n'
        print(head)
        f.write(head)

    return