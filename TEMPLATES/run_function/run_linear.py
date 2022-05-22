import os

import matplotlib.pyplot as plt
import numpy as np

from analysis.linearScanline.linearScanline import linearScanline
from read_write_joints.readJoints import readJoints
from read_write_joints.write_json import write_json
# from workflow.workflow_config import linear_brief, template


def run_linear(template):
    plt.close()

    linear_path = template['LINEAR_OUTPUT']

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

    [frequency, spacing_real, THETA] = linearScanline(nodes, info_scanline)
    # print("Real spacing : {}".format(np.mean(spacing_real)))
    # linear_brief['Real spacing'] = np.mean(spacing_real)
    # print("Mean orientation : {}".format(np.mean(np.rad2deg(THETA))))
    # linear_brief['Mean orientation'] = np.mean(np.mean(np.rad2deg(THETA)))
    # print("Trace length : {}".format(np.mean(nodes['norm'])))
    # linear_brief['Trace length'] = np.mean(nodes['norm'])
    print("Реальный интервал (среднее) : {}".format(np.mean(spacing_real)))
    linear_brief['Реальный интервал (среднее)'] = np.mean(spacing_real)
    print("Угол наклона линии (среднее) : {}".format(np.mean(np.rad2deg(THETA))))
    linear_brief['Угол наклона линии (среднее)'] = np.mean(np.mean(np.rad2deg(THETA)))
    print("Длина линии (среднее) : {}".format(np.mean(nodes['norm'])))
    linear_brief['Длина линии (среднее)'] = np.mean(nodes['norm'])

    write_json(linear_brief, linear_path + os.path.sep + "brief.json")

    return [frequency, spacing_real]
