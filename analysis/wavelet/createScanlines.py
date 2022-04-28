from matplotlib import pyplot as plt
import numpy as np

from analysis.linearScanline.create_scanline import create_scanline
from analysis.linearScanline.find_best_scanline import find_best_scanline
from read_write_joints.nodes2vector import nodes2vector


def createScanlines(nodes, scanline_info, **kwargs):
    nb_scans = scanline_info['nb_scans']
    nb_lines = scanline_info['nb_lines']
    deltaX = scanline_info['dX']
    deltaY = scanline_info['dY']

    if scanline_info['theta'] == -999:  # No orientation given by user
        best_scanline = find_best_scanline(nodes, nb_scans)
    else:
        vector = nodes2vector(nodes)
        # get trace extents
        xminmax = [min(vector['x']), max(vector['x'])]
        yminmax = [min(vector['y']), max(vector['y'])]
        best_scanline = create_scanline(xminmax, yminmax, scanline_info['theta'])

    Xsl = best_scanline['Xsl']
    Ysl = best_scanline['Ysl']
    Xb = best_scanline['Xb']
    Yb = best_scanline['Yb']

    plt.figure(1)
    plt.plot(Xsl[0], Ysl[0], 'k--', linewidth=1)  # plot scanline
    plt.legend(title="Main scanline")
    minX_scanline = np.min(Xsl[1])

    scanline = {"iD": [], "dX": [], "dY": []}
    scanline['iD'].append(0)
    scanline['dX'].append(0)
    scanline['dY'].append(0)

    X = []
    Y = []
    X_trans = []
    for i in range(len(nodes['iD'])):
        intersection = polyxpoly(nodes['x'][i], nodes['y'][i], Xsl[0],Ysl[0]) # find intersection between polyline and scanline

    pass
