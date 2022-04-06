import numpy as np
import matplotlib.pyplot as plt


def polylines_to_lines(nodes):
    id_x1x2y1y2_matrice = np.empty((len(nodes['iD']), 5))
    id_x1x2y1y2_matrice[:] = np.NaN

    nodes['line'] = [*range(len(nodes['iD']))]
    for i in range(len(nodes['iD'])):
        x = nodes['x'][i]
        y = nodes['y'][i]
        p = np.polyfit(x[0], y[0], 1)
        x_1 = np.min(x)
        x_2 = np.max(x)
        y_1 = p[0] * x_1 + p[1]
        y_2 = p[0] * x_2 + p[1]
        nodes['line'][i] = [x_1, x_2, y_1, y_2]
        id_x1x2y1y2_matrice[i, :] = [i, x_1, x_2, y_1, y_2]

        Xl = [x_1, x_2]  # x-coordinate
        Yl = [y_1, y_2]  # y-coordinate

        plt.plot(Xl, Yl, "b-")

    plt.show()
    pass
