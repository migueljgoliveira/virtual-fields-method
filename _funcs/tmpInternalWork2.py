import numpy as np

import _utils

def tmp_internal_work2(strain,rot,rotm,vol,pkstress,ne,dof,ndi,ntens,nf,fout,layers):

    strain = _utils.rotate_tensor(strain,rot,rotm,ne,dof,ndi,ntens,nf,
                                  dir=1,voigt=False,eng=True)

    strain = _utils.flatten_tensor(strain,ne,dof,nf)


    iw1 = 1e-3 * pkstress * strain
    iw2 = 1e-3 * pkstress * strain * vol[None,:,None]

    if dof == 3:
        for i in range(3):
            iwl1 = iw1[:,layers[i],:]
            iwl2 = iw2[:,layers[i],:]
            iwl1 = np.nansum(iwl1,1)
            iwl2 = np.nansum(iwl2,1)

            np.savetxt(f'output\{fout}\{fout}_SED-{i+1}.csv',iwl1,fmt='%.12f',delimiter=';')

            np.savetxt(f'output\{fout}\{fout}_SE-{i+1}.csv',iwl2,fmt='%.12f',delimiter=';')

    iw1 = np.nansum(iw1,1)

    np.savetxt(f'output\{fout}\{fout}_SED.csv',iw1,fmt='%.12f',delimiter=';')

    iw2 = np.nansum(iw2,1)

    np.savetxt(f'output\{fout}\{fout}_SE.csv',iw2,fmt='%.12f',delimiter=';')

    exit()
    return