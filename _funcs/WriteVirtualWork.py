import os
import numpy as np

def write_virtual_work(ivw,evw,test,nvfs,nf,nt,fout,dirout):
    """
    Write internal and external virtual work of final solution.

    Parameters
    ----------
    ivw : (nvfs,nf) , float
        Internal virtual work.
    evw : (nvfs,nf) , float
        External virtual work.
    nvfs : int
        Number of virtual fields.
    nf : int
        Number of increments.
    nt : int
        Number of tests.
    test : str
        Name of test.
    fout : str
        Name of output folder.
    dirout : str
        Directory of project to export output files.
    """

    # Set output directory
    if nt > 1:
        dir = os.path.join(dirout,test)
        fnameivw = os.path.join(dir,f'{test}_IVW.csv')
        fnameevw = os.path.join(dir,f'{test}_EVW.csv')
    else:
        fnameivw = os.path.join(dirout,f'{fout}_IVW.csv')
        fnameevw = os.path.join(dirout,f'{fout}_EVW.csv')

    # Set file header
    head = [f'vf{i+1}' for i in range(nvfs)]
    head = f'inc;{";".join(head)}'

    # Generate formmatter
    fmt = ['%.12e']*nvfs
    fmt.insert(0,'%d')

    # Generate increment number
    incs = np.arange(0,nf)

    # Write internal virtual work
    np.savetxt(fnameivw,np.column_stack((incs,ivw.T)),
                        header=head,fmt=fmt,delimiter=';',comments='')

    # Write external virtual work
    np.savetxt(fnameevw,np.column_stack((incs,evw.T)),
                        header=head,fmt=fmt,delimiter=';',comments='')

    return