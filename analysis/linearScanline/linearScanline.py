import os.path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import MultiLineString, LineString

from analysis.linearScanline.find_best_scanline import find_best_scanline
from utils.nodes2vector import nodes2vector
from utils.plot_nodes import plot_nodes
from utils.selectExtends import selectExtends
import utils.lang as lang
import utils.template as template
from utils.write_plot import write_plot


def linearScanline(nodes, info_scanline):

    vector = nodes2vector(nodes)

    print(lang.select_locale("-- Scanline AUTO --", "-- Автоматическая линенйная развертка --"))
    best_scanline = find_best_scanline(nodes, info_scanline['nbScan']) # automatic scanline selection
    Xsl = np.array(best_scanline['Xsl']).flatten()
    Ysl = np.array(best_scanline['Ysl']).flatten()
    Xb = np.array(best_scanline['Xb']).flatten()
    Yb = np.array(best_scanline['Yb']).flatten()

    polyline_coord = list(np.zeros((len(nodes['x']) - 1, 1)))
    for i in range(len(nodes['x']) - 1):
        polyline_coord[i] = ((nodes['x'][i][0], nodes['y'][i][0]),
                             (nodes['x'][i][1], nodes['y'][i][1]))
    polyline = MultiLineString(polyline_coord)
    scanline = LineString([(Xsl[0], Ysl[0]), (Xsl[1], Ysl[1])])
    intersection = polyline.intersection(scanline)
    xi = [intersection.geoms[i].coords[0][0] for i in range(len(intersection.geoms))]
    yi = [intersection.geoms[i].coords[0][1] for i in range(len(intersection.geoms))]
    XYi = np.vstack((xi, yi)).T

    plt.figure(1)
    plot_nodes(nodes)
    plt.plot(Xsl, Ysl, 'k--', linewidth=1)  # plot scanline
    plt.plot(Xb, Yb, 'g-.', linewidth=1)  # plot scanline extend
    plt.plot(xi, yi, 'rx')  # plot intersection scanline and joints

    # Observation window for synthetic joints
    if nodes['synthetic'] == 1:
        [_, window, nodes] = selectExtends(nodes, 0.1)
        plt.xlim([window['minX'], window['maxX']])
        plt.ylim([window['minY'], window['maxY']])

    # plt.title("Aux Scanline")
    plt.title(lang.select_locale("Aux Scanline", "Вспомогательная сканирующая линия"))
    write_plot(template.config['LINEAR_OUTPUT'])

    # POST-PROCESSING
    # -- joint direction

    THETA = vector['ori']
    north = info_scanline['north'] * 2 * np.pi / 360
    THETA = THETA + north
    THETA[THETA > 2 * np.pi] = THETA[THETA > 2 * np.pi] - 2 * np.pi
    THETA[THETA < 0] = THETA[THETA < 0] + 2 * np.pi
    N = 50
    theta = np.linspace(0.0, np.pi, N, endpoint=False)
    [height1, _] = np.histogram(THETA, N)
    [height2, _] = np.histogram(THETA, N)

    plt.subplots(constrained_layout=True, num=2)
    ax = plt.subplot(polar=True)
    ax.bar(theta, height1, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    ax.bar(theta + np.pi, height2, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge",
           color="darkorange")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.title.set_text(
        lang.select_locale('Rose diagram\n Scanline orientation (°)', 'Роза-диаграмма\n Угол наклона линии (°)'))
    write_plot(template.config['LINEAR_OUTPUT'])

    # -- joint tracelength and spacing
    coord_cross = np.sort((np.vstack((XYi, np.vstack((Xsl, Ysl)).T))), 0)
    spacing_app = np.sqrt(np.diff(coord_cross[:, 0]) ** 2 + np.diff(coord_cross[:, 1]) ** 2)
    spacing_real = spacing_app * np.abs(np.sin(np.pi / 2 - np.mean(THETA) - best_scanline['theta_scanline']))
    frequency = 1 / np.mean(spacing_real)

    print(lang.select_locale('Spacing frequency : {}', 'Частота интервалов : {}').format(frequency))
    template.linear_brief[lang.select_locale('Spacing frequency', 'Частота интервалов')] = frequency

    nbins = 10
    plt.subplots(constrained_layout=True, num=3)
    ax1 = plt.subplot(311, xlabel=lang.select_locale("Trace lengths (m)", "Длина линии (м)"),
                      ylabel=lang.select_locale("Counts", "Кол-во"),
                      title=lang.select_locale("Histogram - Trace length", "Гистограмма - Длина линии"))
    ax1.hist(nodes['norm'], nbins, edgecolor="black")
    ax2 = plt.subplot(312, xlabel=lang.select_locale("Apparent spacing (m)", "Видимый интервал (м)"),
                      ylabel=lang.select_locale("Counts", "Кол-во"),
                      title=lang.select_locale("Histogram - Apparent spacing", "Гистограмма - Видимый интервал"))
    ax2.hist(spacing_app, nbins, edgecolor="black")
    # ax3 = plt.subplot(313, xlabel="Real spacing (m)", ylabel="Counts", title="Histogram - Real spacing")
    ax3 = plt.subplot(313, xlabel=lang.select_locale("Real spacing (m)", "Реальный интервал (м)"),
                      ylabel=lang.select_locale("Counts", "Кол-во"),
                      title=lang.select_locale("Histogram - Real spacing", "Гистограмма - Реальный интервал"))
    ax3.hist(spacing_real, nbins, edgecolor="black")
    write_plot(template.config["LINEAR_OUTPUT"])

    plt.subplots(constrained_layout=True, num=4)
    ax1 = plt.subplot(311, xlabel=lang.select_locale("Orientation (°)", "Угол наклона линии(°)"), ylabel="CDF",
                      title=lang.select_locale("Cumulative distribution - Orientation",
                                               "Кумулятивное распределение - Угол наклона"))
    ori = np.rad2deg(THETA)
    sns.ecdfplot(data=ori, ax=ax1)

    ax2 = plt.subplot(312, xlabel=lang.select_locale("Real spacing (m)", "Реальный интервал (м)"), ylabel="CDF",
                      title=lang.select_locale("Cumulative distribution - Spacing",
                                               "Кумулятивное распределение - Интервал"))
    sns.ecdfplot(data=spacing_real, ax=ax2)

    ax3 = plt.subplot(313, xlabel=lang.select_locale("Trace length (m)", "Длина линии (м)"), ylabel="CDF",
                      title=lang.select_locale("Cumulative distribution - Trace length",
                                               "Кумулятивное распределение - Длинна линии"))
    sns.ecdfplot(data=nodes['norm'], ax=ax3)
    write_plot(template.config["LINEAR_OUTPUT"])

    return [frequency, spacing_real, THETA]
