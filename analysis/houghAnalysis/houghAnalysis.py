import os
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from analysis.houghAnalysis.plot_inHoughFrame import plot_inHoughFrame
import utils.lang as lang
import utils.template as template
from utils.write_plot import write_plot


def houghAnalysis(nodes):
    nodes = plot_inHoughFrame(nodes)
    [mu, sigma] = norm.fit(np.array(nodes['ori_mean_deg']).reshape(-1, 1))
    print(lang.select_locale('Gaussian distribution parameters for orientation: \n mu={} -- sigma={}\n',
                             'Гауссовское распределение параметров угла наклона линии: \n mu={} -- sigma={}\n').format(
        mu, sigma))
    template.hough_brief[lang.select_locale('Gaussian distribution parameters for orientation',
                                            'Гауссовское распределение параметров угла наклона линии')] = {'mu': 0,
                                                                                                           'sigma': 0}
    template.hough_brief[lang.select_locale('Gaussian distribution parameters for orientation',
                                            'Гауссовское распределение параметров угла наклона линии')]['mu'] = mu
    template.hough_brief[lang.select_locale('Gaussian distribution parameters for orientation',
                                            'Гауссовское распределение параметров угла наклона линии')]['sigma'] = sigma

    # Apparent spacing
    r = nodes['r']
    app_spacing = np.empty((1, len(r) - 1))
    app_spacing[:] = np.NaN
    r_theta = np.hstack((np.array(nodes['r']).reshape(-1, 1), np.array(nodes['ori_mean']).reshape(-1, 1)))
    r_theta = r_theta[np.argsort(r_theta[:, 0])]
    real_spacing = np.empty((1, len(r) - 1))
    real_spacing[:] = np.NaN
    for s in range(len(r) - 1):
        app_spacing[0, s] = r_theta[s + 1, 0] - r_theta[s, 0]
        r1 = r_theta[s + 1, 0] - r_theta[s, 0] / np.cos(r_theta[s + 1, 1] - r_theta[s, 1])
        r2 = r_theta[s + 1, 0] / np.cos(r_theta[s + 1, 1] - r_theta[s, 1]) - r_theta[s, 0]
        real_spacing[0, s] = np.mean([r2, r1])

    nodes['real_spacing_hough'] = real_spacing
    nodes['app_spacing_hough'] = app_spacing

    nbins = 10
    plt.subplots(constrained_layout=True, num=3)
    ax1 = plt.subplot(311, xlabel=lang.select_locale('Trace lengths (m)', 'Длина линии (м)'),
                      ylabel=lang.select_locale('Counts', 'Кол-во'))
    ax1.hist(np.array(nodes['norm']), nbins, edgecolor="black")
    ax2 = plt.subplot(312, xlabel=lang.select_locale('Apparent spacing (m)', 'Видимый интервал (м)'),
                      ylabel=lang.select_locale('Counts', 'Кол-во'))
    ax2.hist(np.array(app_spacing).flatten(), nbins, edgecolor="black")
    ax3 = plt.subplot(313, xlabel=lang.select_locale('Real spacing (m)', 'Реальный интервал (м)'),
                      ylabel=lang.select_locale('Counts', 'Кол-во'))
    ax3.hist(np.array(real_spacing).flatten(), nbins, edgecolor="black")

    write_plot(template.config['HOUGH_OUTPUT'])

    return nodes
