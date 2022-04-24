import numpy as np
import matplotlib.pyplot as plt

from read_write_joints.polylines_to_lines import polylines_to_lines
from read_write_joints.selectExtends import selectExtends


def computePersistanceMap(nodes, nbRectangles):
    [_, id_x1x2y1y2_matrice] = polylines_to_lines(nodes)
    id_x1x2y1y2_matrice = id_x1x2y1y2_matrice[:, 1:]
    MEAN_ori = np.mean(nodes['ori_mean_deg'])
    x = id_x1x2y1y2_matrice[:, 0:2]
    y = id_x1x2y1y2_matrice[:, 2:4]

    x1 = x[:, 0]
    x2 = x[:, 1]
    y1 = y[:, 0]
    y2 = y[:, 1]

    d = np.max(((np.max(x) - np.min(x)), (np.max(y) - np.min(y))))  # max distance in x and y direction
    [_, window, _] = selectExtends(nodes, 0.1)
    xmin = window['minX']
    xmax = window['maxX']
    ymin = window['minY']
    ymax = window['maxY']
    plt.xlim([window.minX,window.maxX])
    plt.ylim([window.minY,window.maxY])

    pass
