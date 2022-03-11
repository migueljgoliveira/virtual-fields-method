import os
import shutil

def create_directory(out):
    """
    Create directory to export output files of current project.

    Parameters
    ----------
    out : str
        Name of output folder.

    Returns
    -------
    dir : str
        Directory of project to export output files.
    """

    cwd = os.getcwd()
    dir = f'{cwd}\\output\\{out}'
    if os.path.isdir(dir):
        shutil.rmtree(dir)

    os.mkdir(dir)

