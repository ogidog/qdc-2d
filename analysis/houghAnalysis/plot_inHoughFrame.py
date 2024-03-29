import os

import matplotlib.pyplot as plt
import numpy as np

from utils.polylines_to_lines import polylines_to_lines
import utils.lang as lang
import utils.template as template
from utils.write_plot import write_plot


def plot_inHoughFrame(nodes):

    plt.figure(1)
    # Create Hough matrix from nodes
    [nodes, *_] = polylines_to_lines(nodes)
    plt.title(lang.select_locale('Hough transform', 'Трансформация Хафа'))
    plt.xlabel('Theta')
    plt.ylabel('r')

    write_plot(template.config['HOUGH_OUTPUT'])

    plt.figure(2)
    nodes['r'] = [*range(len(nodes['iD']))]
    for j in range(len(nodes['iD'])):
        x = nodes['line'][j][0]
        y = nodes['line'][j][2]
        nodes['r'][j] = np.abs(
            y * np.cos(np.radians(nodes['ori_mean_deg'][j])) - x * np.sin(np.radians(nodes['ori_mean_deg'][j])))
        plt.plot(nodes['ori_mean_deg'][j], nodes['r'][j], 'r.')
        plt.title(lang.select_locale("Distribution of the orientation mean degree",
                                     "Распределение средних значений угла наклона"))

    write_plot(template.config['HOUGH_OUTPUT'])

    return nodes
