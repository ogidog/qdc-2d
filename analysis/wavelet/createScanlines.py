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

    Xsl = np.array(best_scanline['Xsl']).flatten()
    Ysl = np.array(best_scanline['Ysl']).flatten()
    Xb = np.array(best_scanline['Xb']).flatten()
    Yb = np.array(best_scanline['Yb']).flatten()

    plt.plot(Xsl, Ysl, 'k--', linewidth=1, label="Main scanline")  # plot scanline
    minX_scanline = np.min(Xsl[1])

    scanline = {"iD": [], "dX": [], "dY": []}
    scanline['iD'].append(0)
    scanline['dX'].append(0)
    scanline['dY'].append(0)

    X = []
    Y = []
    X_trans = []
    line1 = LineString([(Xsl[0], Ysl[0]), (Xsl[1], Ysl[1])])
    for i in range(len(nodes['iD'])):
        line2 = LineString([(nodes['x'][i][0], nodes['y'][i][0]), (nodes['x'][i][1], nodes['y'][i][1])])
        intersection = line1.intersection(line2)  # find intersection between polyline and scanline
        if intersection.geom_type == "LineString": continue
        # scanline['cross'] = [xi,yi]
        [xi, yi] = [intersection.x, intersection.y]
        X.append(xi)
        Y.append(yi)
        X_trans.append(np.sqrt((xi - minX_scanline) ** 2 + (yi - np.min(Ysl)) ** 2))

    scanline['X'] = [X]
    scanline['Y'] = [Y]
    scanline['X_trans'] = [X_trans]
    scanline['minY'] = [np.min(Ysl)]
    scanline['maxY'] = [np.max(Ysl)]
    scanline['minX'] = [np.min(Xsl)]
    scanline['maxX'] = [np.max(Xsl)]

    # Secondary scanline
    for line in range(1, int(nb_lines) + 1):
        scanline['iD'].append(-1 * line)
        scanline['dX'].append(line * deltaX)
        scanline['dY'].append(-1 * line * deltaY)
        scanline['iD'].append(line)
        scanline['dX'].append(-1 * line * deltaX)
        scanline['dY'].append(line * deltaY)

        # Y translate
        minY_scanline_up = np.min(Ysl) + line * deltaY
        minY_scanline_down = np.min(Ysl) - line * deltaY
        maxY_scanline_up = np.max(Ysl) + line * deltaY
        maxY_scanline_down = np.max(Ysl) - line * deltaY
        scanline['minY'].append(minY_scanline_down)
        scanline['minY'].append(minY_scanline_up)
        scanline['maxY'].append(maxY_scanline_down)
        scanline['maxY'].append(maxY_scanline_up)

        # X translate
        minX_scanline_up = np.min(Xsl) + line * deltaX
        minX_scanline_down = np.min(Xsl) - line * deltaX
        maxX_scanline_up = np.max(Xsl) + line * deltaX
        maxX_scanline_down = np.max(Xsl) - line * deltaX
        scanline['minX'].append(minX_scanline_down)
        scanline['minX'].append(minX_scanline_up)
        scanline['maxX'].append(maxX_scanline_down)
        scanline['maxX'].append(maxX_scanline_up)

        X_up = []
        Y_up = []
        X_trans_up = []
        X_down = []
        Y_down = []
        X_trans_down = []

        txt_up = 'dX : -{} ---- dY: {}'.format(line * deltaX, line * deltaY)
        txt_down = 'dX : {} ---- dY: -{}'.format(line * deltaX, line * deltaY)
        plt.plot(Xsl - line * deltaX, Ysl + line * deltaY, '--', linewidth=1, label=txt_up)  # plot scanlines
        plt.plot(Xsl + line * deltaX, Ysl - line * deltaY, '--', linewidth=1, label=txt_down)  # plot scanlines
        line1 = LineString(
            [(Xsl[0] - line * deltaX, Ysl[0] + line * deltaY), (Xsl[1] - line * deltaX, Ysl[1]) + line * deltaY])
        line2 = LineString(
            [(Xsl[0] + line * deltaX, Ysl[0] - line * deltaY), (Xsl[1] + line * deltaX, Ysl[1]) - line * deltaY])
        for i in range(nodes['iD']):
            line3 = LineString([(nodes['x'][i][0], nodes['y'][i][0]), (nodes['x'][i][1], nodes['y'][i][1])])

            intersection = line2.intersection(line3)  # find intersection between polyline and scanline
            #X_down       = [X_down xi]
            #Y_down       = [Y_down yi]
            #X_trans_down = [X_trans_down sqrt((xi-minX_scanline).^2 + (yi-minY_scanline_down).^2)]; %#ok<AGROW>
            #scanline.X{2*line}       = X_down;
            #scanline.Y{2*line}       = Y_down;
            #scanline.X_trans{2*line} = X_trans_down;

            intersection = line1.intersection(line3)  # find intersection between polyline and scanline
            if intersection.geom_type == "Point":
                [xi, yi] = [intersection.x, intersection.y]
                X_up.append(xi)
                Y_up.append(yi)
                X_trans_up.append(np.sqrt((xi - minX_scanline) ** 2 + (yi - minY_scanline_up) ** 2))
                scanline['X'].append(X_up)
                scanline['Y'].append(Y_up)
                scanline['X_trans'].append(X_trans_up)

        pass

    plt.legend(loc="best")
