import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from inspect import signature
from shapely.geometry import LineString, MultiLineString

from utils.plot_lines import plot_lines
from utils.polylines_to_lines import polylines_to_lines
from utils.selectExtends import selectExtends

import utils.lang as lang
import utils.template as template


def computePersistence(nodes, covering):

    f = signature(computePersistence)
    if len(f.parameters) == 2:
        if covering > 1 or covering < 0:
            print(lang.select_locale("Covering parameters should be [0, 1]", 'Коэффициент покрытия должны быть в интервале [0, 1]'))
            sys.exit(1)

    plt.figure(1)
    [nodes, id_x1x2y1y2_matrice, *_] = polylines_to_lines(nodes)
    id_x1x2y1y2_matrice = id_x1x2y1y2_matrice[:, 1:]
    plt.clf()
    plt.cla()
    plot_lines(nodes)
    plt.title(lang.select_locale('I -- Persistence over the entire window', 'I -- Расчет постоянства по всему окну'))

    MEAN_ori = np.mean(nodes['ori_mean_deg'])
    print(lang.select_locale('Mean joint orientation (°) : {}', 'Угол наклона линии (°) : {}').format(MEAN_ori))
    wfc.persistence_brief[lang.select_locale('Mean joint orientation', 'Угол наклона линии')] = MEAN_ori

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

    if len(f.parameters) == 2:
        print(lang.select_locale('Input covering argument given : {}', 'Задан коэффициент покрытия : {}').format(template.config['COVER']))
        # Square side value - c
        c = covering * np.min(np.array([y_max - y_min, x_max - x_min]))
        xw = np.mean(np.array([x_max, x_min]))
        yw = np.mean(np.array([y_max, y_min]))
        squares = {}
        squares['x1'] = xw - c / 2
        squares['x2'] = xw + c / 2
        squares['y1'] = yw - c / 2
        squares['y2'] = yw + c / 2
        square = {}
        square['h'] = c
        square['L'] = c
    else:
        print(lang.select_locale('No covering argument', 'Не задан коэффициент покрытия'))

    # Plot middle of the square
    plt.plot(xw, yw, 'rx')

    # Plot square
    x_Square = np.array([squares['x1'], squares['x1'], squares['x2'], squares['x2'], squares['x1']])
    y_Square = np.array([squares['y1'], squares['y2'], squares['y2'], squares['y1'], squares['y1']])
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
            xy = np.array([[intersection.geoms[i].x, intersection.geoms[i].y] for i in range(len(intersection.geoms))])
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

            if x_min > np.min(x_Square) and x_max < np.max(x_Square) and y_min > np.min(y_Square) and y_max < np.max(
                    y_Square):
                n_tot_cc = n_tot_cc + 1
                n_inter_cc = n_inter_cc + 1

    plt.savefig(template.config["PERSISTENCE_OUTPUT"] + os.path.sep + "fig1_" + str(wfc.classif_joint_set_counter) + ".png",
                dpi=300)
    plt.show()

    if (n_tot_cc - n_trans_cc + n_inter_cc) > 0:
        persistance_cc = square['L'] * square['h'] / (
                    square['h'] * np.sin(math.radians(MEAN_ori)) + square['L'] * np.cos(math.radians(MEAN_ori))) * (
                                     n_tot_cc + n_trans_cc - n_inter_cc) / (n_tot_cc - n_trans_cc + n_inter_cc)
        n_tot = n_tot_cc
        n_trans = n_trans_cc
        n_inter =  n_inter_cc
        persistance = persistance_cc

    print(lang.select_locale('Total joints : {}', 'Всего линий : {}').format(n_tot))
    wfc.persistence_brief[lang.select_locale('Total joints', 'Всего линий')] = n_tot

    print(lang.select_locale('Inter joints : {}', 'Внутренних линий в покрытии: {}').format(n_inter))
    wfc.persistence_brief[lang.select_locale('Inter joints', 'Внутренних линий в покрытии')] = n_inter

    print(lang.select_locale('Transection joints : {}', 'Поперечные линии в покрытии : {}').format(n_trans))
    wfc.persistence_brief[lang.select_locale('Transection joints', 'Поперечные линии в покрытии')] = n_trans

    print(lang.select_locale('Mean persistance : {}', 'Коэффициент постоянства (среднее) : {}').format(np.mean(persistance)))
    wfc.persistence_brief[
        lang.select_locale('Mean persistance', 'Коэффициент постоянства (среднее)')] = np.mean(persistance)

    return persistance