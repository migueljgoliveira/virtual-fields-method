import sys
import numpy as np

spc = ' '
fmt = '.12e'

def print_write(out,flog,end='\n'):

    print(out,end=end)
    flog.write(f'{out}{end}')

    return

def close_log_file(flog):

    flog.close()

def open_log_file(fout,mode='a'):

    return open(f'output\{fout}\{fout}.log',mode)

def print_iteration(it,fout):
    """
    Print and write iteration header to command window and log file.

    Parameters
    ----------
    it : int
        Iteration number.
    fout : str
        Name of output folder.
    """

    # Open log file
    flog = open_log_file(fout)

    print_write('\n',flog)

    # Print iteration header
    if it == 0:
        ithead = f' Initial '
        lit = -3
    else:
        ithead = f' Iteration {it} '
        lit = len(str(it))

    sep = '-'*len(ithead)

    print_write(f'{spc*(15-lit)}{sep}',flog)
    print_write(f'{spc*(15-lit)}{ithead}',flog)
    if it == 0:
        print_write(f'{spc*(15-lit)}{sep}',flog,end='')
    else:
        print_write(f'{spc*(15-lit)}{sep}\n',flog)

    # Close log file
    close_log_file(flog)

    return

def print_progress(it,feit,x,phi,nvars,nt,fout,type):
    """
    Print and write identification progress to command window and log file.

    Parameters
    ----------
    it : int
        Iteration number.
    feit : int
        Current number of evaliation in iteration.
    x : (nvars,) , float
        Current iteration identification variables.
    phi : (nt,) , float
        Current iteratiom cost function.
    nvars : int
        Number of identification variables.
    nt : int
        Number of tests.
    fout : str
        Name of output folder.
    """

    # Open log file for read
    flog = open_log_file(fout,mode='r+')

    # Read log file contents
    fdata = flog.readlines()

    # Set number of lines to bring cursor up
    if nt > 1:
        cursor = 9 + 3 + nt
    else:
        cursor = 9

    # Write log file contents without last evaluation
    if feit != 1 and (not (feit == 2 and it == 1)):

        # Open log file for write
        flog = open_log_file(fout,mode='w')

        # Write log file contents up to cursor line
        flog.writelines(fdata[:-cursor])

    # Open log file for append
    flog = open_log_file(fout,mode='a')

    # Print current number of evaluations in iteration
    if it > 0:
        lfeit = len(str(feit))
        feithead = f'  Evaluations {spc*(13-lfeit)}{feit}'
        print_write(feithead,flog,end='')

    # Print variables
    varhead = f'\n\n  Variables\n'
    print_write(varhead,flog)
    for i in range(nvars):
        vl = len(str(i+1))
        var = f' {i+1}{spc*(5+vl)}{x[i]:{fmt}}'
        print_write(f' {var}',flog)

    # Print cost function
    if nt > 1:
        costhead = f'\n  Cost\n'
        print_write(costhead,flog)
        for i in range(nt):
            cl = len(str(i+1))
            cost = f' {i+1}{spc*(5+cl)}{phi[i]:{fmt}}'
            print_write(f' {cost}',flog)

        cost = f'\n  Total  {np.sum(phi):{fmt}}'
        print_write(f' {cost}',flog)
    else:
        costhead = f'\n  Cost{spc*3}{np.sum(phi):{fmt}}'
        print_write(costhead,flog)

    # Move console cursor to evaluations line during iteration
    if (it > 0) and (type == 'fe'):
        sys.stdout.write("\033[F"*cursor)

    # Close log file
    close_log_file(flog)

    return