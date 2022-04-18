import numpy as np
import matplotlib.pyplot as plt

# plt.ion()
# fig = plt.figure()

def plot_progress(it,bestphi):

    plt.plot(it,np.sum(bestphi),'.')

    return