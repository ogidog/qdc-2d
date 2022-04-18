import numpy as np
import matplotlib.pyplot as plt

from analysis.linearScanline.scanlineSelection import scanlineSelection
from read_write_joints.nodes2vector import nodes2vector
from read_write_joints.plot_nodes import plot_nodes
from read_write_joints.selectExtends import selectExtends


def linearScanline(nodes, info_scanline):
    vector = nodes2vector(nodes)

    # TODO: uncomment
    # prompt = 'Automatic scanline estimation? \n -- 0:automatic \n -- 1:click 2 points  \n -- 2:1point and 1 orientation \n'
    # autoScanline_bool = input(prompt)
    autoScanline_bool = 0

    # [best_scanline, intersection_x, intersection_y] = scanlineSelection(autoScanline_bool, nodes,
    #                                                                   info_scanline['nbScan'])
    # Xsl = np.array(best_scanline['Xsl']).flatten()
    # Ysl = np.array(best_scanline['Ysl']).flatten()
    # Xb = np.array(best_scanline['Xb']).flatten()
    # Yb = np.array(best_scanline['Yb']).flatten()

    # plot_nodes(nodes, plt)
    # plt.plot(Xsl, Ysl, 'k--', linewidth=1)  # plot scanline
    # plt.plot(Xb, Yb, 'g-.', linewidth=1)  # plot scanline extend
    # plt.plot(intersection_x, intersection_y, 'rx')  # plot intersection scanline and joints

    # Observation window for synthetic joints
    # if nodes['synthetic'] == 1:
    #    [_, window, nodes] = selectExtends(nodes, 0.1)
    #    plt.xlim([window['minX'], window['maxX']])
    #    plt.ylim([window['minY'], window['maxY']])

    # plt.show()

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

    ax = plt.subplot(polar=True)
    ax.bar(theta, height1, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    ax.bar(theta + np.pi, height2, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge",
           color="darkorange")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.title.set_text('Rose diagram (°)')
    plt.show()

# return [frequency, spacing_real, THETA]
