import os.path

import numpy as np
from scipy.optimize import fmin_bfgs
from matplotlib import pyplot as plt

from classify._withHistograms.computeGaussians import computeGaussians
from classify._withHistograms.minimizeFunction import minimizeFunction
from classify._withHistograms.smoothHisto import smoothHisto
import utils.template as template
import utils.lang as lang


def find_jointSet_fromHistogram():
    theta_vector = [*range(1, 181, 2)]

    # plt.figure(1)
    # theta = nodes['ori_mean']
    # N = 50
    # x = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    # [y, _] = np.histogram(np.array([np.array(theta), np.array(theta) + np.pi]), N)
    # ax = plt.subplot(polar=True)
    # ax.bar(x, y, bottom=0.0, width=2 * np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    # plt.show()

    plt.figure(2)
    plt.subplots(constrained_layout=True)
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title(lang.select_locale('Estimated result', 'Оценочные результаты'))
    ax1.set_xlabel(lang.select_locale('Orientation (°)', 'Угол наклона линии (°)'))
    ax1.set_ylabel(lang.select_locale('Counts', 'Кол-во'))
    ax1.plot(theta_vector, wfc.nodes['oriHisto'], '--', color=[0.5, 0.5, 0],
             label=lang.select_locale("Raw data", "Исходные данные"))  # plot tracelength
    XTick = np.arange(0, 190, 10)
    ax1.set_xtick = XTick
    # Plot smoothed data
    theta_histogram_smoothed = smoothHisto(wfc.nodes['oriHisto'], 10)
    ax1.plot(theta_vector, theta_histogram_smoothed, '-', color=[1, 0, 0],
             label=lang.select_locale("Smoothed data", "Аппроксимация"))
    ax1.legend()

    # -- USER estimation
    # gaussian_param_esti = jointSet_estimation_byUser()
    # -- From template file
    gaussian_param_esti = {}
    gaussian_param_esti['G_mean'] = template.config['G_MEAN']
    gaussian_param_esti['G_std'] = template.config['G_STD']
    gaussian_param_esti['G_N'] = template.config['G_N']
    gaussian_param_esti['noise'] = template.config['G_NOISE']
    gaussian_param_esti['NBjointSet'] = len(template.config['G_MEAN'])

    # Create Gaussian curves
    gaussians = computeGaussians(gaussian_param_esti)

    # Plot first estimation
    for curve in range(np.size(gaussians['curves'], axis=1)):
        plt.plot(np.array(theta_vector), gaussians['curves'][:, curve].flatten())
    plt.plot(theta_vector, gaussians['sum'], linewidth=2)

    # -- Optimization
    theta_histogram = wfc.nodes['oriHisto']
    w0 = [gaussian_param_esti['noise']]
    w0.extend(gaussian_param_esti['G_mean'])
    w0.extend(gaussian_param_esti['G_std'])
    w0.extend(gaussian_param_esti['G_N'])

    w = fmin_bfgs(minimizeFunction, w0, args=(theta_histogram,), disp=False)
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title(lang.select_locale('Optimization result', 'Результат оптимизации'))
    ax2.set_xlabel(lang.select_locale('Orientation (°)', 'Угол наклона линии (°)'))
    ax2.set_ylabel(lang.select_locale('Counts', 'Кол-во'))
    ax2.plot(theta_vector, theta_histogram, '-', color=[1, 0, 0])
    ax2.set_xtick = XTick

    gaussian_param_OPT = gaussian_param_esti
    NBjointSet = gaussian_param_OPT['NBjointSet']
    gaussian_param_OPT['G_mean'] = w[1:NBjointSet + 1]
    gaussian_param_OPT['G_std'] = w[NBjointSet + 1:2 * NBjointSet + 1]
    gaussian_param_OPT['G_N'] = w[2 * NBjointSet + 1:3 * NBjointSet + 1]
    gaussian_param_OPT['noise'] = w[1]
    gaussians_OPT = computeGaussians(gaussian_param_OPT)

    for curve in range(np.size(gaussians_OPT['curves'], 1)):
        ax2.plot(theta_vector, gaussians_OPT['curves'][:, curve])
    ax2.plot(theta_vector, gaussians_OPT['sum'], linewidth=2)

    plt.savefig(template.config['OPTIMIZATION_OUTPUT'] + os.path.sep + 'fig1.png', dpi=300)
    plt.show()

    # --  RESUME
    print(lang.select_locale('End of histogram optimization!\n', 'Оптимизация завершена\n'))
    print(lang.select_locale('-- Results are : \n', '-- Результаты : \n'))

    print(lang.select_locale('Noise estimation : {}\n', 'Оценка шума : {}\n').format(w[1]))
    wfc.optimization_brief[lang.select_locale('Noise estimation', 'Оценка шума')] = w[1]

    wfc.optimization_brief[lang.select_locale('Joints', 'Наборы линий')] = []

    for j in range(NBjointSet):
        optimized_joints = {}

        print(lang.select_locale('Joint #{}', 'Набор линий №{}').format(j + 1))
        optimized_joints[lang.select_locale('Joint', 'Набор линий №')] = j + 1

        print(lang.select_locale('Mean: {}  --  ', 'Среднее: {}  --  ').format(w[j + 1]))
        optimized_joints[lang.select_locale('Mean', 'Среднее')] = w[j + 1]

        print(lang.select_locale('Standard deviation : {}  --  ', 'Дисперсия : {}  --  ').format(w[NBjointSet + j + 1]))
        optimized_joints[lang.select_locale('Standard deviation', 'Дисперсия')] = w[NBjointSet + j + 1]

        print(lang.select_locale('Amplitude : {}', 'Средняя амплитуда : {}').format(w[2 * NBjointSet + j + 1]))
        optimized_joints[lang.select_locale('Amplitude', 'Средняя амплитуда')] = w[2 * NBjointSet + j + 1]

        wfc.optimization_brief[lang.select_locale('Joints', 'Наборы линий')].append(optimized_joints)

        print(' ')

    return gaussian_param_OPT
