import os

import numpy as np
from matplotlib import pyplot as plt

from analysis.blockVolume_estimation.compute_Jv import compute_Jv
from analysis.blockVolume_estimation.compute_volume import compute_volume
import utils.template as template
from utils.write_json import write_json


def volume():
    plt.close()

    if 'jORIENTATION' in template.config.keys() and 'jSPACING' in template.config.keys():
        orientation = np.array(template.config['jORIENTATION']).flatten()
        spacing = np.array(template.config['jSPACING']).flatten()
        jointSetInfo = np.array([orientation, spacing], dtype="int").T
    else:
        return

    if not os.path.exists(template.config['VOLUME_OUTPUT']):
        os.makedirs(template.config['VOLUME_OUTPUT'])

    compute_volume(jointSetInfo)
    compute_Jv(jointSetInfo)

    write_json(template.volume_brief, template.config['VOLUME_OUTPUT'])
