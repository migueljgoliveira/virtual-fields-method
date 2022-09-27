import numpy as np

import _utils

def tmp_internal_work(strain,rot,rotm,vol,stress,ne,dof,ndi,ntens,nf,fout,surfElem):

    stress = _utils.tensor_to_voigt(stress,ne,ndi,ntens,nf)

    strain = _utils.rotate_tensor(strain,rot,rotm,ne,dof,ndi,ntens,nf,
                                  dir=1,voigt=True,eng=True)

    iw = stress * strain * vol[None,:,None]
    iw = np.nansum(iw,1)

    np.savetxt(f'output\{fout}\{fout}_IW.csv',iw,fmt='%.12f',delimiter=';')

    # if dof == 3:
    #     iw = stress * strain
    #     iwSurf = iw[:,surfElem]
    #     iwSurf = np.nansum(iwSurf,1)

    #     np.savetxt(f'output\{fout}\{fout}_IWSurf.csv',iwSurf,fmt='%.12f',delimiter=';')

    #     iw = stress * strain * vol[None,:,None]
    #     iwSurf = iw[:,surfElem]
    #     iwSurf = np.nansum(iwSurf,1)

    #     np.savetxt(f'output\{fout}\{fout}_IWSurf-Vol.csv',iwSurf,fmt='%.12f',delimiter=';')


    exit()
    return