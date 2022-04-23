import numpy as np
import matplotlib.pyplot as plt

from read_write_joints.nodes2vector import nodes2vector


def polylines_to_lines(nodes):
    id_x1x2y1y2_matrice = np.empty((len(nodes['iD']), 5))
    id_x1x2y1y2_matrice[:] = np.NaN

    nodes['line'] = [*range(len(nodes['iD']))]
    for i in range(len(nodes['iD'])):
        x = nodes['x'][i]
        y = nodes['y'][i]
        p = np.polyfit(x, y, 1)
        x_1 = np.min(x)
        x_2 = np.max(x)
        y_1 = p[0] * x_1 + p[1]
        y_2 = p[0] * x_2 + p[1]
        nodes['line'][i] = [x_1, x_2, y_1, y_2]
        id_x1x2y1y2_matrice[i, :] = [i, x_1, x_2, y_1, y_2]

        Xl = [x_1, x_2]  # x-coordinate
        Yl = [y_1, y_2]  # y-coordinate

        plt.plot(Xl, Yl, "b-")

    # Extend of the window
    vector = nodes2vector(nodes)
    xmoy = (np.min(vector['x']) + np.max(vector['x'])) / 2
    ymoy = (np.min(vector['y']) + np.max(vector['y'])) / 2
    # Find the max trace length
    # the extend will be the 1/2 of max trace length
    norm = nodes['norm']
    sortedX = sorted(norm[:], reverse=True)
    top3 = sortedX[2]
    max_extend = top3/2
    n = 2
    plt.xlim([xmoy-max_extend/n, xmoy+max_extend/n])
    plt.ylim([ymoy-max_extend/n, ymoy+max_extend/n])

    return [nodes, id_x1x2y1y2_matrice]
