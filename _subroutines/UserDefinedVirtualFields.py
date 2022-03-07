import numpy as np

def UserDefinedVirtualFields(coord,nvfs,ne):

    vfields = {'ivw': np.zeros((nvfs,ne,2,2)),
               'evw': np.zeros(nvfs,2)}

    
    return vfields