import numpy as np

spc = ' '
fmt = '.12e'

def print_write(out,f):

    print(out)
    f.write(f'{out}\n')

    return

def print_progress(it,x,bestx,phi,bestphi,nvars,nt,fout):
    """
    Print and write identification progress to command window and log file.

    Parameters
    ----------
    it : int
        Evaluation number.
    x : (nvars,) , float
        Current iteration identification variables.
    bestx : (nvars,) , float
        Current best identification variables.
    phi : (nt,) , float
        Current iteratiom cost function.
    bestphi : (nt,) , float
        Current best cost function.
    nvars : int
        Number of identification variables.
    nt : int
        Number of tests.
    fout : str
        Name of output folder.
    """

    # Open log file
    f = open(f'output\{fout}\{fout}.log','a')

    print_write('\n',f)

    # Print evaluation header
    ithead = f' Evaluation {it} '
    sep = '-'*len(ithead)
    print_write(f' {sep}',f)
    print_write(f' {ithead}',f)
    print_write(f' {sep}',f)

    # Print information header
    infohead = f'{spc*19} Current {spc*16} Best'
    print_write(infohead,f)

    # Print variables
    varhead = f'  X\n'
    print_write(varhead,f)
    for i in range(nvars):
        vl = len(str(i+1))
        var = f' {i+1}{spc*(5+vl)}{x[i]:{fmt}}{spc*4}{bestx[i]:{fmt}}'
        print_write(f' {var}',f)

    # Print cost function
    if nt > 1:
        costhead = f'\n  Cost\n'
        print_write(costhead,f)
        for i in range(nt):
            cl = len(str(i+1))
            cost = f' {i+1}{spc*(5+cl)}{phi[i]:{fmt}}{spc*4}{bestphi[i]:{fmt}}'
            print_write(f' {cost}',f)

        cost = f'\n  Total  {np.sum(phi):{fmt}}{spc*4}{np.sum(bestphi):{fmt}}'
        print_write(f' {cost}',f)
    else:
        costhead = f'\n  Cost{spc*3}{np.sum(phi):{fmt}}{spc*4}{np.sum(bestphi):{fmt}}'
        print_write(costhead,f)

    # Close log file
    f.close()

    return

def print_result(nit,bestx,bestphi,tmsg,nvars,nt,fout):
    """
    Print and write identification result to command window and log file.

    Parameters
    ----------
    nit : int
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
    """

    # Open log file
    f = open(f'output\{fout}\{fout}.log','a')

    print_write('\n',f)

    # Print summary header
    ithead = f' Summary '
    sep = '-'*len(ithead)
    print_write(f' {sep}',f)
    print_write(f' {ithead}',f)
    print_write(f' {sep}',f)

    # Print termination message
    tmsg = f'\n  Termination : {tmsg}'
    print_write(tmsg,f)

    # Print number of evaluations
    evalhead = f'  Evaluations : {nit}'
    print_write(evalhead,f)

    # Print information header
    infohead = f'\n{spc*22} Best'
    print_write(infohead,f)

    # Print variables
    varhead = f'  X\n'
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