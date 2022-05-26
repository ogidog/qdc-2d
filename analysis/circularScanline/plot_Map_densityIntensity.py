import os

import numpy as np
from matplotlib import pyplot as plt
import utils.lang as lang
import workflow.workflow_config as wfc


def plot_Map_densityIntensity(xw, yw, intensity_vect, density_vect, dx):
    plt.figure(2)

    # Intensity map plot
    plt.subplots(constrained_layout=True)
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

    plt.savefig(wfc.template["CIRCULAR_OUTPUT"] + os.path.sep + "fig2_" + str(wfc.classif_joint_set_counter) + ".png",
                dpi=300)
    plt.show()
