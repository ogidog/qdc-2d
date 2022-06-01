import os

import numpy as np
from matplotlib import pyplot as plt
import utils.lang as lang
import utils.template as template
from utils.write_plot import write_plot


def plot_Map_densityIntensity(xw, yw, intensity_vect, density_vect, dx):
    # Intensity map plot
    plt.subplots(constrained_layout=True, num=2)
    plt.subplot(211)
    plt.imshow(intensity_vect.reshape((len(np.unique(yw)), len(np.unique(xw)))),
               extent=[np.min(xw), np.max(xw), np.max(yw), np.min(yw)], aspect='auto')
    plt.colorbar()
    plt.title(lang.select_locale('Intensity map', 'Карта интенсивности'))
    ax = plt.gca()
    ax.invert_yaxis()

    # Density map plot
    plt.subplot(212)
    plt.imshow(density_vect.reshape((len(np.unique(yw)), len(np.unique(xw)))),
               extent=[np.min(xw), np.max(xw), np.max(yw), np.min(yw)], aspect='auto')
    plt.colorbar()
    plt.title(lang.select_locale('Intensity map', 'Карта плотности'))
    ax = plt.gca()
    ax.invert_yaxis()

    write_plot(template.config["CIRCULAR_OUTPUT"])
