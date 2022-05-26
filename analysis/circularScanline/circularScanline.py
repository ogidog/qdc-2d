import os

import numpy as np
from matplotlib import pyplot as plt

from analysis.circularScanline.intersectCT import intersectCT
from analysis.circularScanline.plot_Map_densityIntensity import plot_Map_densityIntensity
from utils.polylines_to_lines import polylines_to_lines
from utils.selectExtends import selectExtends
import utils.template as template
import utils.lang as lang


def circularScanline(nodes, nbCircles):
    plt.figure(1)

    [_, id_x1x2y1y2_matrice] = polylines_to_lines(nodes)
    id_x1x2y1y2_matrice = id_x1x2y1y2_matrice[:, 1:]
    x = id_x1x2y1y2_matrice[:, 0:2]
    dx = x[:, 0] - x[:, 1]
    y = id_x1x2y1y2_matrice[:, 2:]
    dy = y[:, 0] - y[:, 1]

    lT = np.sqrt(dx ** 2 + dy ** 2)  # length of trace
    x1 = x[:, 0]
    x2 = x[:, 1]
    y1 = y[:, 0]
    y2 = y[:, 1]

    d = max(np.max(x) - np.min(x), np.max(y) - np.min(y))  # max distance in x and y direction
    [extends, window, _] = selectExtends(nodes, 0.01)
    xmin = window['minX']
    xmax = window['maxX']
    ymin = window['minY']
    ymax = window['maxY']

    dx = max((xmax - xmin), (ymax - ymin)) / (nbCircles - 1)  # interval/diameter of circles
    [xw, yw] = np.meshgrid(np.arange(xmin + dx / 2, xmax + dx / 2, dx / 2),
                           np.arange(ymin + dx / 2, ymax, dx / 2))  # mesh of circles
    xw = xw.T.flatten()
    yw = yw.T.flatten()
    R = dx / 2  # radius of circles

    s = {'xC': [], 'yC': [], 'xT': [], 'yT': [], 'xTC': [], 'yTC': [], 'm': []}
    for nc in range(len(xw)):  # Analysis for each circle
        # CIRCLE INTERSECT
        # circle coor
        xc = xw[nc]
        yc = yw[nc]
        # translate to the origin
        x_1 = x1 - xc
        x_2 = x2 - xc
        y_1 = y1 - yc
        y_2 = y2 - yc

        # Points intersecting the circle
        [xTC, yTC, k] = intersectCT(x_1, x_2, y_1, y_2, R, lT, [], [], 1, 1)
        [xTC, yTC, _] = intersectCT(x_1, x_2, y_1, y_2, R, lT, xTC, yTC, k, -1)

        # ENDPOINT WITHIN CIRCLE
        d = [np.sqrt(x_1 ** 2 + y_1 ** 2), np.sqrt(x_2 ** 2 + y_2 ** 2)]
        endpoints = np.where(d < R)[1]  # points within the circle
        xendpoint = np.append(x_1, x_2)
        yendpoint = np.append(y_1, y_2)
        # keep points within the circle
        xendpoint = xendpoint[endpoints] + xc
        yendpoint = yendpoint[endpoints] + yc

        # SAVE --> for plotting
        s['xC'].append(xc + R * np.cos(
            np.arange(0, 2 * np.pi + 2 * np.pi / 100, 2 * np.pi / 100)))  # points of the circle (for plotting)
        s['yC'].append(yc + R * np.sin(np.arange(0, 2 * np.pi + 2 * np.pi / 100, 2 * np.pi / 100)))
        s['xT'].append(np.vstack((x_1, x_2)).T + xc)
        s['yT'].append(np.vstack((y_1, y_2)).T + yc)
        s['xTC'].append(xTC + xc)  # Points intersection circle/joint
        s['yTC'].append(yTC + yc)
        s['m'].append(np.vstack((xendpoint, yendpoint)).T)  # points within circle

    n = 0
    m = 0
    density_vect = np.zeros(len(xw))
    intensity_vect = np.zeros(len(xw))
    for c in range(len(xw)):  # for each circle
        if (len(s['xTC'][c]) > 0):  # if points within/intersect the circle
            x = s['m'][c]  # points within
            n = n + len(s['xTC'][c])  # nb of intersections joint/circles
            m = m + np.size(x, 0)  # nb of points within the circle
            density_vect[c] = np.size(x, 0)
            intensity_vect[c] = len(s['xTC'][c])
            if np.mod(c, 2) != 0:
                plt.plot(s['xC'][c], s['yC'][c], 'y--', linewidth=0.5)
                plt.plot(xw[c], yw[c], 'yx')  # plot circle center and plot circles
            else:
                plt.plot(s['xC'][c], s['yC'][c], 'k-')
                plt.plot(xw[c], yw[c], 'kx')  # plot circle center
            plt.plot(s['xT'][c].T, s['yT'][c].T, 'b-', linewidth=1.5)  # plot joints
            plt.plot(s['xTC'][c], s['yTC'][c], 'rx', linewidth=2)  # plot intersections
            plt.plot(x[:, 0], x[:, 1], 'go', linewidth=2)  # plot points within circles

    # Window selection
    plt.xlim([extends['minX'], extends['maxX']])
    plt.ylim([extends['minY'], extends['maxY']])
    plt.title(lang.select_locale("Circular Window Sampling", "Выборка по окну окружности"))
    plt.savefig(template.config["CIRCULAR_OUTPUT"] + os.path.sep + "fig1_" + str(wfc.classif_joint_set_counter) + ".png",
                dpi=300)
    plt.show()

    m = m / c  # mean points within circles
    n = n / c  # mean intersections

    # -- Estimator calculation
    intensity_estimator = n / (4 * R)  # n/4r
    density_estimator = m / (2 * np.pi * R)  # m/2pr
    traceLength_estimator = (n / m) * np.pi * R / 2  # (n/m)pr/2

    print(lang.select_locale('Mean intensity estimator : {}', 'Оценка интенсивности (среднее) : {}').format(
        intensity_estimator))
    wfc.circular_brief[
        lang.select_locale('Mean intensity estimator', 'Оценка интенсивности (среднее)')] = intensity_estimator

    print(
        lang.select_locale('Mean density estimator : {}', 'Оценка плотности (среднее) : {}').format(density_estimator))
    wfc.circular_brief[lang.select_locale('Mean density estimator', 'Оценка плотности (среднее)')] = density_estimator

    print(lang.select_locale('Mean trace length estimator : {}', 'Оценка длины линий (среднее) : {}').format(
        traceLength_estimator))
    wfc.circular_brief[
        lang.select_locale('Mean trace length estimator', 'Оценка длины линий (среднее)')] = traceLength_estimator

    print(' ')

    print(lang.select_locale('Mean/std intensity : {} / {}',
                             'Среднее/Дисперсия (интенсивность) : {} / {}').format(np.mean(intensity_vect),
                                                                                   np.std(intensity_vect)))
    wfc.circular_brief[lang.select_locale('Mean/std intensity', 'Среднее/Дисперсия (интенсивность)')] = str(
        np.mean(intensity_vect)) + " / " + str(np.std(intensity_vect))

    print(lang.select_locale('Mean/std density : {} / {}', 'Cреднее/Дисперсия (плотность) : {} / {}').format(
        np.mean(density_vect), np.std(density_vect)))
    wfc.circular_brief[lang.select_locale('Mean/std density', 'Cреднее/Дисперсия (плотность)')] = str(
        np.mean(density_vect)) + " / " + str(np.std(density_vect))

    plot_Map_densityIntensity(xw, yw, intensity_vect, density_vect, dx)

    return [intensity_estimator, density_estimator, traceLength_estimator]
