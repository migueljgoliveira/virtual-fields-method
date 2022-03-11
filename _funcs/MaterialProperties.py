import numpy as np

def material_properties():

    # Double-Notched-2D
    props = np.array([
                      0,
                      0, 200000.0, 0.3,
                      1, 0.257171, 0.357013, 0.642987, 1.5, 1.5, 2.75409,
                      1, 256.0, 855.0,
                      0,
                      0
                      ])

    # CurvedBar
    # props = np.array([
    #                   0,
    #                   0, 200000.0, 0.3,
    #                   0,
    #                   2, 565.0, 0.780877350642e-2, 0.26,
    #                   0,
    #                   0
    #                   ])

    nprops = len(props)

    return props,nprops