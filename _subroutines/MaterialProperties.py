import numpy as np

def MaterialProperties():

    # Elastic example
    # props = np.array([
    #                   0,
    #                   0, 210000.0, 0.3,
    #                   0,
    #                   0,100,
    #                   0,
    #                   0
    #                   ])

    # Plastic example
    props = np.array([
                      0,
                      0, 210000.0, 0.3,
                      0,
                      2, 565.0, 7.81e-3, 0.26,
                      0,
                      0
                      ])

    nprops = len(props)

    return props,nprops