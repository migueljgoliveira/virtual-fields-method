import os
import numpy as np

def write_progress(it,fevit,x,phi,nvars,nt,fout):
    """
    Write identification progress of variables and cost function. 

    Parameters
    ----------
    it : int
        Iteration number.
    fevit : int
        Total number of function evaluations in iteration.
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
    fname = f'{dir}\{fout}_Progress.csv'

    # Generate formmatter
    if nt > 1:
        fmt = ['%.12e']*(nvars+1+nt)
    else:
        fmt = ['%.12e']*(nvars+1)
    fmt.insert(0,'%d')
    fmt.insert(0,'%d')

    # If first evaluation create file
    if not os.path.exists(fname):

        # Generate header
        head = f'it;fe;phi'

        if nt > 1:
            for i in range(nt):
                head = head + f';phi{i+1}'

        if len(x) > 9:
            headx = [f'x{i+1}' for i in range(nvars)]
        else:
            headx = [f'x{i+1}' for i in range(nvars)]

        head = f'{head};{";".join(headx)}'

        # Insert cost function
        if nt > 1:
            lout = np.insert(x,0,phi)
            lout = np.insert(lout,0,np.sum(phi))
        else:
            lout = np.insert(x,0,phi)

        # Insert total number of evaluations in iteration
        lout = np.insert(lout,0,fevit)

        # Insert iteration number
        lout = np.insert(lout,0,it)

        # Write header and first iteration result
        np.savetxt(fname,[lout],header=head,fmt=fmt,delimiter=';',comments='')

    # Append subsequent evaluations
    else:

        # Insert cost function
        if nt > 1:
            lout = np.insert(x,0,phi)
            lout = np.insert(lout,0,np.sum(phi))
        else:
            lout = np.insert(x,0,phi)

        # Insert total number of evaluations in iteration
        lout = np.insert(lout,0,fevit)

        # Insert iteration number
        lout = np.insert(lout,0,it)

        # Append iteration result
        with open(fname,'a') as f:
            np.savetxt(f,[lout],fmt=fmt,delimiter=';')

    return