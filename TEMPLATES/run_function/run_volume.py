import os

import numpy as np
from matplotlib import pyplot as plt

from analysis.blockVolume_estimation.compute_Jv import compute_Jv
from analysis.blockVolume_estimation.compute_volume import compute_volume


def run_volume(template):
    plt.close()

    if 'jORIENTATION' in template.keys() and 'jSPACING' in template.keys():
        orientation = np.array(template['jORIENTATION']).flatten()
        spacing = np.array(template['jSPACING']).flatten()
        jointSetInfo = np.array([orientation, spacing], dtype="int").T
    else:
        return

    if not os.path.exists(template['VOLUME_OUTPUT']):
        os.makedirs(template['VOLUME_OUTPUT'])

    compute_volume(jointSetInfo)
    compute_Jv(jointSetInfo)
