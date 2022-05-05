import numpy as np
from matplotlib import pyplot as plt


def plot_Map_densityIntensity(xw, yw, intensity_vect, density_vect, dx):

    plt.figure(2)

    # Intensity map plot
    plt.subplots(constrained_layout=True)
    plt.subplot(211)
    plt.imshow(intensity_vect.reshape((len(np.unique(yw)), len(np.unique(xw)))), extent=[np.min(xw), np.max(xw), np.max(yw), np.min(yw)], aspect='auto')
    plt.colorbar()
    plt.title('Intensity map')
    ax = plt.gca()
    ax.invert_yaxis()

    # Density map plot
    plt.subplot(212)
    plt.imshow(density_vect.reshape((len(np.unique(yw)), len(np.unique(xw)))), extent=[np.min(xw), np.max(xw), np.max(yw), np.min(yw)],aspect='auto')
    plt.colorbar()
    plt.title('Density map')
    ax = plt.gca()
    ax.invert_yaxis()

    plt.show()
