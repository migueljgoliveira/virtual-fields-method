import time
from datetime import datetime

def print_start(prjname,fout,dirout):
    """
    Print and write start info to log file.

    Parameters
    ----------
    prjname: str
        Name of current project.
    fout : str
        Name of output folder.
    dirout : str
        Directory of project to export output files.

    Returns
    -------
    st : float
        Start time in seconds since epoch.
    """

    # Get start time
    st = time.time()

    # Get current date and time
    now = datetime.now()

    # Create log file
    with open(f'{dirout}\{fout}.log','w') as f:
        head = f'\n  ~ VIRTUAL FIELDS METHOD ~\n'
        print(head)
        f.write(head)

        prj = f'  Project : {prjname}'
        print(prj)
        f.write(f'\n{prj}')

        date = f'  Date : {now.date()}'
        print(date)
        f.write(f'\n{date}')

        stime = f'  Start Time : {now.hour}h{now.minute:02d}m'
        print(stime)
        f.write(f'\n{stime}')

    return st