import numpy as np


def selectExtends(nodes, extend):
    id_x1x2y1y2_matrice = np.empty((len(nodes['iD']), 5))
    id_x1x2y1y2_matrice[:] = np.NaN

    VALUE = extend

    nodes['middle'] = np.zeros((len(nodes['iD']), 2))
    for i in range(len(nodes['iD'])):
        x = nodes['x'][i][0]
        y = nodes['y'][i][0]
        p = np.polyfit(x, y, 1)
        x_1 = np.min(x)
        x_2 = np.max(x)
        y_1 = p[0] * x_1 + p[1]
        y_2 = p[0] * x_2 + p[1]
        x_moy = (x_1 + x_2) / 2
        y_moy = (y_1 + y_2) / 2
        nodes['middle'][i] = [x_moy, y_moy]

    # Min/max of the middle
    extends = {}
    middle_min = np.amin(nodes['middle'], axis=0, where=True)
    middle_max = np.amax(nodes['middle'], axis=0, where=True)
    extends['minX'] = middle_min[0]
    extends['minY'] = middle_min[1]
    extends['maxX'] = middle_max[0]
    extends['maxY'] = middle_max[1]

    # Extends of the window
    window = {}
    window['minX'] = extends['minX'] + VALUE * (extends['maxX'] - extends['minX'])
    window['minY'] = extends['minY'] + VALUE * (extends['maxY'] - extends['minY'])
    window['maxX'] = extends['maxX'] - VALUE * (extends['maxX'] - extends['minX'])
    window['maxY'] = extends['maxY'] - VALUE * (extends['maxY'] - extends['minY'])

    return [extends, window, nodes]
