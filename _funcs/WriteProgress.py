import os
import numpy as np

def write_progress(x,phi,nvars,nt,fout,best=''):

    """
    Parameters
    ----------
    x : (nvars,) , float
        Current or best identification variables.
    phi : (nt,) , float
        Current or best cost function.
    nvars : int
        Number of identification variables.
    nt : int
        Number of tests.
    fout : str
        Name of output folder.
    """

    # Set output directory
    dir = f'output\{fout}'
    fname = f'{dir}\{fout}_Progress{best}.csv'

    # Generate formmatter
    if nt > 1:
        fmt = ['%22.8f']*(nvars+1+nt)
    else:
        fmt = ['%22.8f']*(nvars+1)
    fmt.insert(0,'%10d')

    # If first evaluation create file
    if not os.path.exists(fname):

        # Generate header
        head = f'{"":<6}eval;{"":<19}phi'

        if nt > 1:
            for i in range(nt):
                head = head + f';{"":<18}phi{i+1}'

        if len(x) > 9:
            headx = [f'{"":<19}x{i+1}' for i in range(nvars)]
        else:
            headx = [f'{"":<20}x{i+1}' for i in range(nvars)]

        head = f'{head};{";".join(headx)}'

        # Insert cost function
        lout = np.insert(x,0,phi)

        # Insert evaluation number
        lout = np.insert(lout,0,1)

        # Write header and first evaluation result
        np.savetxt(fname,[lout],header=head,fmt=fmt,delimiter=';',comments='')

    # Append subsequent evaluations
    else:

        # Load previous evalution number
        fe = np.loadtxt(fname,skiprows=1,ndmin=1,usecols=0,delimiter=';')[-1]

        # Insert cost function
        lout = np.insert(x,0,phi)

        # Insert evaluation number
        lout = np.insert(lout,0,fe+1)

        # Append evaluation result
        with open(fname,'a') as f:
            np.savetxt(f,[lout],fmt=fmt,delimiter=';')

    return