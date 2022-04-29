from matplotlib import pyplot as plt
import numpy as np
from shapely.geometry import LineString

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
    line1 = LineString([(Xsl[0][0], Ysl[0][0]), (Xsl[1][0], Ysl[1][0])])
    for i in range(len(nodes['iD'])):
        line2 = LineString([(nodes['x'][i][0], nodes['y'][i][0]), (nodes['x'][i][1], nodes['y'][i][1])])
        intersection = line1.intersection(line2)  # find intersection between polyline and scanline
        if intersection.geom_type == "LineString": continue
        # scanline['cross'] = [xi,yi]
        [xi, yi] = [intersection.x, intersection.y]
        X.append(xi)
        Y.append(yi)
        X_trans.append(np.sqrt((xi - minX_scanline) ** 2 + (yi - np.min(Ysl)) ** 2))

    scanline['X'] = X
    scanline['Y'] = Y
    scanline['X_trans'] = X_trans
    scanline['minY'] = np.min(Ysl)
    scanline['maxY'] = np.max(Ysl)
    scanline['minX'] = np.min(Xsl)
    scanline['maxX'] = np.max(Xsl)

    # Secondary scanline
    for line in range(1, int(nb_lines) + 1):
        scanline['iD'].append(-1 * line)
        scanline['dX'].append(line * deltaX)
        scanline['dY'].append(-1 * line * deltaY)
        scanline['iD'].append(line)
        scanline['dX'].append(-1 * line * deltaX)
        scanline['dY'].append(line * deltaY)

    pass
