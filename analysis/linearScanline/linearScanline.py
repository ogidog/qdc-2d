import os.path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import MultiLineString, LineString

from analysis.linearScanline.scanlineSelection import scanlineSelection
from read_write_joints.nodes2vector import nodes2vector
from read_write_joints.plot_nodes import plot_nodes
from read_write_joints.selectExtends import selectExtends


def linearScanline(nodes, info_scanline):

    linear_path = template['LINEAR_OUTPUT']

    vector = nodes2vector(nodes)

    autoScanline_bool = 0
    best_scanline = scanlineSelection(autoScanline_bool, nodes, info_scanline['nbScan'])
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
    plt.title("Линейная развертка")
    plt.savefig(linear_path + os.path.sep + "fig1.png", dpi=300)
    plt.show()

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

    plt.figure(2)
    plt.subplots(constrained_layout=True)
    ax = plt.subplot(polar=True)
    ax.bar(theta, height1, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    ax.bar(theta + np.pi, height2, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge",
           color="darkorange")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    # ax.title.set_text('Rose diagram (°)')
    ax.title.set_text('Роза-диаграмма \n Угол наклона линии (°)')
    plt.savefig(linear_path + os.path.sep + "fig2.png", dpi=300)
    plt.show()

    # -- joint tracelength and spacing
    coord_cross = np.sort((np.vstack((XYi, np.vstack((Xsl, Ysl)).T))), 0)
    spacing_app = np.sqrt(np.diff(coord_cross[:, 0]) ** 2 + np.diff(coord_cross[:, 1]) ** 2)
    spacing_real = spacing_app * np.abs(np.sin(np.pi / 2 - np.mean(THETA) - best_scanline['theta_scanline']))
    frequency = 1 / np.mean(spacing_real)
    # print('Spacing frequency : {}'.format(frequency))
    # linear_brief['Spacing frequency'] = frequency
    print('Частота интервалов : {}'.format(frequency))
    linear_brief['Частота интервалов'] = frequency

    plt.figure(3)
    nbins = 10
    plt.subplots(constrained_layout=True)
    # ax1 = plt.subplot(311, xlabel="Trace lengths (m)", ylabel="Counts", title="Histogram - Trace length")
    ax1 = plt.subplot(311, xlabel="Длина линии (м)", ylabel="Кол-во", title="Гистограмма - Длина линии")
    ax1.hist(nodes['norm'], nbins, edgecolor="black")
    # ax2 = plt.subplot(312, xlabel="Apparent spacing (m)", ylabel="Counts", title="Histogram - Apparent spacing")
    ax2 = plt.subplot(312, xlabel="Видимый интервал (м)", ylabel="Кол-во", title="Гистограмма - Видимый интервал")
    ax2.hist(spacing_app, nbins, edgecolor="black")
    # ax3 = plt.subplot(313, xlabel="Real spacing (m)", ylabel="Counts", title="Histogram - Real spacing")
    ax3 = plt.subplot(313, xlabel="Реальный интервал (м)", ylabel="Кол-во", title="Гистограмма - Реальный интервал")
    ax3.hist(spacing_real, nbins, edgecolor="black")
    plt.savefig(linear_path + os.path.sep + "fig3.png", dpi=300)
    plt.show()

    plt.figure(4)
    plt.subplots(constrained_layout=True)
    # ax1 = plt.subplot(311, xlabel="Orientation (°)", ylabel="CDF", title="Cumulative distribution - Orientation")
    ax1 = plt.subplot(311, xlabel="Угол наклона (°)", ylabel="CDF", title="Кумулятивное распределение - Угол наклона")
    ori = np.rad2deg(THETA)
    sns.ecdfplot(data=ori, ax=ax1)
    # ax2 = plt.subplot(312, xlabel="Real spacing (m)", ylabel="CDF", title="Cumulative distribution - Spacing")
    ax2 = plt.subplot(312, xlabel="Реальный интервал (м)", ylabel="CDF", title="Кумулятивное распределение - Интервал")
    sns.ecdfplot(data=spacing_real, ax=ax2)
    # ax3 = plt.subplot(313, xlabel="Trace length (m)", ylabel="CDF", title="Cumulative distribution - Trace length")
    ax3 = plt.subplot(313, xlabel="Длина линии (м)", ylabel="CDF", title="Кумулятивное распределение - Длинна линии")
    sns.ecdfplot(data=nodes['norm'], ax=ax3)
    plt.savefig(linear_path + os.path.sep + "fig4.png", dpi=300)
    plt.show()

    return [frequency, spacing_real, THETA]
