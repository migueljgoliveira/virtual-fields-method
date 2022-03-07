import numpy as np

def MaterialProperties():

    props = np.array([
                      0,
                      0, 210000.0, 0.3,
                      0,
                      0,100,
                      0,
                      0
                      ])

    nprops = len(props)

    return props,nprops