import numpy as np

from analysis.linearScanline.linearScanline import linearScanline
from read_write_joints.readJoints import readJoints


def run_linear(template):
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

    linearScanline(nodes, info_scanline)
    #[_, spacing_real, THETA] = linearScanline(nodes, info_scanline)
    #print("\nReal spacing : {}\n".format(np.mean(spacing_real)))
    #print("\nMean orientation : {}\n".format(np.mean(np.rad2deg(THETA))))
    #print("\nTrace length : {}\n".format(np.mean(nodes['norm'])))

    pass
