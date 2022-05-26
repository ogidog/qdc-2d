import os

import numpy as np
import matplotlib.pyplot as plt
import math
from shapely.geometry import LineString, MultiLineString

from utils.polylines_to_lines import polylines_to_lines
from utils.selectExtends import selectExtends

import utils.template as template
import utils.lang as lang


def computePersistanceMap(nodes, nbRectangles):
    plt.figure(2)
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
    plt.xlim([window['minX'], window['maxX']])
    plt.ylim([window['minY'], window['maxY']])

    # create rectangles
    dx = np.min(((xmax - xmin), (ymax - ymin))) / (nbRectangles - 1)  # interval between 2squares
    [xw, yw] = np.meshgrid(np.arange(xmin + dx / 2, xmax - dx / 2, dx / 2),
                           np.arange(ymin + dx / 2, ymax, dx / 2))  # mesh of squares
    xw = xw.flatten(order="F")  # x coordinate of middle square
    yw = yw.flatten(order="F")  # y coordinate of middle square

    persistence_vect = np.zeros(len(xw))
    for i in range(len(xw)):
        x1 = xw[i] - dx / 2
        x2 = xw[i] + dx / 2
        y1 = yw[i] - dx / 2
        y2 = yw[i] + dx / 2
        h = dx
        L = dx
        # Plot middle of the square
        plt.plot(xw[i], yw[i], 'rx')
        # Plot square
        x_Square = [x1, x1, x2, x2, x1]
        y_Square = [y1, y2, y2, y1, y1]

        if np.mod(i, 2) == 0:
            plt.plot(x_Square, y_Square, 'y--', linewidth=0.5)
        else:
            plt.plot(x_Square, y_Square, 'k-')

        n_tot = []
        n_trans = []
        n_inter = []
        persistance = []

        # Analysis intersection
        n_tot_cc = 0
        n_trans_cc = 0
        n_inter_cc = 0

        for j in range(len(id_x1x2y1y2_matrice)):
            poly_X = id_x1x2y1y2_matrice[j][0:2]
            poly_Y = id_x1x2y1y2_matrice[j][2:4]
            poly_line = LineString(((poly_X[0], poly_Y[0]), (poly_X[1], poly_Y[1])))
            square_side_lines = [((x_Square[i], y_Square[i]), (x_Square[i + 1], y_Square[i + 1])) for i in
                                 range(len(x_Square) - 1)]
            square_lines = MultiLineString(square_side_lines)
            intersection = poly_line.intersection(square_lines)
            if intersection.geom_type == "Point":
                xT = [intersection.x]
                yT = [intersection.y]
            elif intersection.geom_type == "LineString":
                xT = []
                yT = []
            elif intersection.geom_type == "MultiPoint":
                xy = np.array(
                    [[intersection.geoms[i].x, intersection.geoms[i].y] for i in range(len(intersection.geoms))])
                xT = xy[:, 0]
                yT = xy[:, 1]

            plt.plot(xT, yT, 'go', linewidth=0.5, fillstyle="none")

            if len(xT) == 1:
                n_tot_cc = n_tot_cc + 1
            elif len(xT) == 2:
                n_trans_cc = n_trans_cc + 1
                n_tot_cc = n_tot_cc + 1
            else:  # no intersection - check if joint is within
                x_min = np.min(poly_X)
                x_max = np.max(poly_X)
                y_min = np.min(poly_Y)
                y_max = np.max(poly_Y)

                if x_min > np.min(x_Square) and x_max < np.max(x_Square) and y_min > np.min(
                        y_Square) and y_max < np.max(
                    y_Square):
                    n_tot_cc = n_tot_cc + 1
                    n_inter_cc = n_inter_cc + 1

        if (n_tot_cc - n_trans_cc + n_inter_cc) > 0:
            persistance = L * h / (h * np.sin(math.radians(MEAN_ori)) + L * np.cos(math.radians(MEAN_ori))) * (
                    n_tot_cc + n_trans_cc - n_inter_cc) / (n_tot_cc - n_trans_cc + n_inter_cc)
            n_tot = n_tot_cc
            n_trans = n_trans_cc
            n_inter = n_inter_cc
            persistence_vect[i] = persistance
        else:
            persistence_vect[i] = 0

    plt.savefig(
        template.config["PERSISTENCE_OUTPUT"] + os.path.sep + "fig2_" + str(wfc.classif_joint_set_counter) + ".png",
        dpi=300)
    plt.show()

    mean_persistence = np.mean(persistence_vect)
    std_persistence = np.std(persistence_vect)

    # Density map plot
    fig3 = plt.figure(3)
    xw_uniq = np.unique(xw)
    yw_uniq = np.unique(yw)
    plt.imshow(np.rot90(persistence_vect.reshape(len(xw_uniq), len(np.unique(yw_uniq))), k=2),
               extent=[np.min(xw_uniq), np.max(xw_uniq), np.max(yw_uniq), np.min(yw_uniq)])
    plt.colorbar()
    ax = plt.gca()
    ax.invert_yaxis()
    str_titleMap = lang.select_locale('Persistence map\nMean persistence : {}\nStd persistence : {}',
                                      'Карта постоянства\nСреднее : {}\nДисперсия : {}').format(
        mean_persistence, std_persistence)

    plt.title(str_titleMap)
    fig3.tight_layout()

    plt.savefig(
        template.config["PERSISTENCE_OUTPUT"] + os.path.sep + "fig3_" + str(wfc.classif_joint_set_counter) + ".png",
        dpi=300)
    plt.show()
