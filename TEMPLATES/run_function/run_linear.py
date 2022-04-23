import matplotlib.pyplot as plt
import numpy as np

from analysis.linearScanline.linearScanline import linearScanline
from read_write_joints.readJoints import readJoints


def run_linear(template):
    plt.close()

    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT (mandatory)')
        return

    info_scanline = {}
    if 'NORTH' in template.keys():
        info_scanline['north'] = template['NORTH']
        print('North orientation given. Joints rotation')
    else:
        info_scanline['north'] = 0

    nodes = readJoints(joint_file)
    nodes['synthetic'] = template['SYNTHETIC']

    info_scanline['nbScan'] = 30

    [_, spacing_real, THETA] = linearScanline(nodes, info_scanline)
    print("Real spacing : {}".format(np.mean(spacing_real)))
    print("Mean orientation : {}".format(np.mean(np.rad2deg(THETA))))
    print("Trace length : {}".format(np.mean(nodes['norm'])))
