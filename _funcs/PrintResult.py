import sys
import time
import numpy as np

spc = ' '
fmt = '.12e'

def convert_time(tt):

    seconds = tt % (24 * 3600)
    hour = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f'{hour:02d}h{minutes:02d}m{seconds:02d}s'

def print_write(out,f):

    print(out)
    f.write(f'{out}\n')

    return

def print_result_identification(nit,nfe,bestx,bestphi,tmsg,nvars,nt,fout,st):
    """
    Print and write results to command window and log file.

    Parameters
    ----------
    nit : int
        Number of iteration.
    nfe : int
        Number of evaluations.
    bestx : (nvars,) , float
        Final best identification variables.
    bestphi : (nt,) , float
        Final best cost function.
    tmsg : str
        Algorithm termination message.
    nvars : int
        Number of identification variables.
    nt : int
        Number of tests.
    fout : str
        Name of output folder.
    st : float
        Start time in seconds since epoch.
    """

    # Open log file
    f = open(f'output\{fout}\{fout}.log','a')

    # Set number of lines to bring cursor up
    if nt > 1:
        cursor = 9 + 3 + nt
    else:
        cursor = 9

    # Move console cursor to evaluations line during iteration
    sys.stdout.write(f"\033[{cursor}B")

    print_write('\n',f)

    # Print summary header
    ithead = f' Summary '
    sep = '-'*len(ithead)
    print_write(f'{spc*18}{sep}',f)
    print_write(f'{spc*18}{ithead}',f)
    print_write(f'{spc*18}{sep}',f)

    # Print termination message
    tmsg = f'\n  Termination : {tmsg}'
    print_write(tmsg,f)

    # Print number of iterations
    evalhead = f'  Iterations : {nit}'
    print_write(evalhead,f)

    # Print number of evaluations
    evalhead = f'  Evaluations : {nfe}'
    print_write(evalhead,f)

    # Print total time
    timehead = f'  Time : {convert_time(time.time() - st)}'
    print_write(timehead,f)

    # Print best variables
    varhead = f'\n  Best Variables\n'
    print_write(varhead,f)
    for i in range(nvars):
        vl = len(str(i+1))
        var = f' {i+1}{spc*(5+vl)}{bestx[i]:{fmt}}'
        print_write(f' {var}',f)

    # Print cost function
    if nt > 1:
        costhead = f'\n  Cost\n'
        print_write(costhead,f)
        for i in range(nt):
            cl = len(str(i+1))
            cost = f' {i+1}{spc*(5+cl)}{bestphi[i]:{fmt}}'
            print_write(f' {cost}',f)

        cost = f'\n  Total  {np.sum(bestphi):{fmt}}'
        print_write(f' {cost}',f)
    else:
        costhead = f'\n  Cost{spc*3}{np.sum(bestphi):{fmt}}'
        print_write(costhead,f)

    # Close log file
    f.close()

    return

def print_result_simulation(phi,nt,fout,st):
    """
    Print and write results to command window and log file.

    Parameters
    ----------
    phi : (nt,) , float
        Cost function.
    nt : int
        Number of tests.
    fout : str
        Name of output folder.
    st : float
        Start time in seconds since epoch.
    """

    # Open log file
    f = open(f'output\{fout}\{fout}.log','a')

    print_write('\n',f)

    # Print summary header
    ithead = f' Summary '
    sep = '-'*len(ithead)
    print_write(f'{spc*18}{sep}',f)
    print_write(f'{spc*18}{ithead}',f)
    print_write(f'{spc*18}{sep}',f)

    # Print cost function
    if nt > 1:
        costhead = f'\n  Cost\n'
        print_write(costhead,f)
        for i in range(nt):
            cl = len(str(i+1))
            cost = f' {i+1}{spc*(5+cl)}{phi[i]:{fmt}}'
            print_write(f' {cost}',f)

        cost = f'\n  Total  {np.sum(phi):{fmt}}'
        print_write(f' {cost}',f)
    else:
        costhead = f'\n  Cost{spc*3}{np.sum(phi):{fmt}}'
        print_write(costhead,f)

    # Close log file
    f.close()

    return