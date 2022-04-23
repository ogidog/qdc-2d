import sys
import matplotlib.pyplot as plt
import numpy as np
from inspect import signature

from read_write_joints.plot_lines import plot_lines
from read_write_joints.polylines_to_lines import polylines_to_lines
from read_write_joints.selectExtends import selectExtends


def computePersistence(nodes, covering):
    # %Check covering is [0 1]

    f = signature(computePersistence)
    if len(f.parameters) == 2:
        if covering > 1 or covering < 0:
            print("Covering parameters should be [0 1]")
            sys.exit(1)

    [nodes, id_x1x2y1y2_matrice, *_] = polylines_to_lines(nodes)
    id_x1x2y1y2_matrice = id_x1x2y1y2_matrice[:, 1:]
    plt.clf()
    plt.cla()
    plot_lines(nodes)
    plt.title('I-- Persistence over the entire window')

    MEAN_ori = np.mean(nodes['ori_mean_deg'])
    print('Mean joint orientation : {} deg'.format(MEAN_ori))

    # Observation window for synthetic joints
    if nodes['synthetic']:
        [_, window, _] = selectExtends(nodes, 0.1)
        x_min = window['minX']
        x_max = window['maxX']
        y_min = window['minY']
        y_max = window['maxY']
        plt.xlim([window['minX'], window['maxX']])
        plt.ylim([window['minY'], window['maxY']])
    else:
        C = nodes['x']
        maxLengthCell = np.max([len(C[i]) for i in range(len(C))])  # finding the longest vector in the cell array
        for i in range(len(nodes['x'])):
            nodes['x'][i] = np.resize(nodes['x'][i], maxLengthCell)
        x_min = np.min(nodes['x'])
        x_max = np.max(nodes['x'])
        y_min = np.min(nodes['y'])
        y_max = np.max(nodes['y'])
