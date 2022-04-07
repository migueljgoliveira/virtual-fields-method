import os
import numpy as np

def write_progress(it,x,phi,nvars,nt,fout,best=''):

    """
    Parameters
    ----------
    it : int
        Iteration number.
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
        fmt = ['%.12e']*(nvars+1+nt)
    else:
        fmt = ['%.12e']*(nvars+1)
    fmt.insert(0,'%d')

    # If first evaluation create file
    if not os.path.exists(fname):

        # Generate header
        head = f'eval;phi'

        if nt > 1:
            for i in range(nt):
                head = head + f';phi{i+1}'

        if len(x) > 9:
            headx = [f'x{i+1}' for i in range(nvars)]
        else:
            headx = [f'x{i+1}' for i in range(nvars)]

        head = f'{head};{";".join(headx)}'

        # Insert cost function
        lout = np.insert(x,0,phi)

        # Insert evaluation number
        lout = np.insert(lout,0,it)

        # Write header and first evaluation result
        np.savetxt(fname,[lout],header=head,fmt=fmt,delimiter=';',comments='')

    # Append subsequent evaluations
    else:

        # Insert cost function
        lout = np.insert(x,0,phi)

        # Insert evaluation number
        lout = np.insert(lout,0,it)

        # Append evaluation result
        with open(fname,'a') as f:
            np.savetxt(f,[lout],fmt=fmt,delimiter=';')

    return