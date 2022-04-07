
def print_write(out,f):

    print(out)
    f.write(f'{out}\n')

    return

def print_progress(it,x,bestx,phi,bestphi,nvars,fout):
    """
    Print and write progress to command window and log file.

    Parameters
    ----------
    it : int
        Iteration number.
    x : (nvars,) , float
        Current iteration identification variables.
    bestx : (nvars,) , float
        Current best identification variables.
    phi : float
        Current iteratiom cost function.
    bestphi : float
        Current best cost function.
    nvars : int
        Number of identification variables.
    fout : str
        Name of output folder.
    """

    spc = ' '
    fmt = '.12e'

    # Open log file
    f = open(f'output\{fout}\{fout}.log','a')

    print_write('\n',f)

    # Print iteration header
    ithead = f' Evaluation {it} '
    sep = '-'*len(ithead)
    print_write(f' {sep}',f)
    print_write(f' {ithead}',f)
    print_write(f' {sep}',f)

    # Print information header
    infohead = f'\n  X {spc*4} Current {spc*13} Best\n'
    print_write(infohead,f)

    # Print variables
    for i in range(nvars):
        vl = len(str(i+1))
        var = f' {i+1} {spc*(3+vl)} {x[i]:{fmt}} {spc*2} {bestx[i]:{fmt}}'
        print_write(f' {var}',f)

    # Print cost function
    costhead = f'\n  Cost {spc*1} {phi:{fmt}} {spc*2} {bestphi:{fmt}}'
    print_write(costhead,f)

    # Close log file
    f.close()

    return