import numpy as np
from scipy.optimize import fmin_bfgs
from matplotlib import pyplot as plt

from classify._withHistograms.computeGaussians import computeGaussians
from classify._withHistograms.jointSet_estimation_byUser import jointSet_estimation_byUser
from classify._withHistograms.minimizeFunction import minimizeFunction
from classify._withHistograms.smoothHisto import smoothHisto

global theta_vector
global theta_histogram


def find_jointSet_fromHistogram(nodes, template):

    theta_vector = [*range(1, 181, 2)]

    plt.figure(1)
    theta = nodes['ori_mean']
    N = 50
    x = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    [y, _] = np.histogram(np.array([np.array(theta), np.array(theta) + np.pi]), N)
    ax = plt.subplot(polar=True)
    ax.bar(x, y, bottom=0.0, width=2 * np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    plt.show()

    plt.figure(2)
    plt.subplots(constrained_layout=True)
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title('Estimated result')
    ax1.set_xlabel('Orientation (degrees)')
    ax1.set_ylabel('Counts')
    ax1.plot(theta_vector, nodes['oriHisto'], '--', color=[0.5, 0.5, 0], label="Raw data")  # plot tracelength
    XTick = np.arange(0, 190, 10)
    ax1.set_xtick = XTick
    # Plot smoothed data
    theta_histogram_smoothed = smoothHisto(nodes['oriHisto'], 10)
    ax1.plot(theta_vector, theta_histogram_smoothed, '-', color=[1, 0, 0], label="Smoothed data")
    ax1.legend()

    # -- USER estimation
    # gaussian_param_esti = jointSet_estimation_byUser()
    # -- From template file
    gaussian_param_esti = {}
    gaussian_param_esti['G_mean'] = template['G_mean']
    gaussian_param_esti['G_std'] = template['G_std']
    gaussian_param_esti['G_N'] = template['G_N']
    gaussian_param_esti['noise'] = template['G_noise']
    gaussian_param_esti['NBjointSet'] = len(template['G_mean'])

    # Create Gaussian curves
    gaussians = computeGaussians(gaussian_param_esti)

    # Plot first estimation
    for curve in range(np.size(gaussians['curves'], axis=1)):
        plt.plot(np.array(theta_vector), gaussians['curves'][:, curve].flatten())
    plt.plot(theta_vector, gaussians['sum'], linewidth=2)

    # -- Optimization
    theta_histogram = nodes['oriHisto']
    w0 = [gaussian_param_esti['noise']]
    w0.extend(gaussian_param_esti['G_mean'])
    w0.extend(gaussian_param_esti['G_std'])
    w0.extend(gaussian_param_esti['G_N'])

    w = fmin_bfgs(minimizeFunction, w0, args=(theta_histogram,))
    ax2 = plt.subplot(2, 1, 2)
    ax2.set_title('Optimization result')
    ax2.set_xlabel('Orientation (degrees)')
    ax2.set_ylabel('Counts')
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

    plt.show()

    # --  RESUME
    print('End of histogram optimization!\n -- \nResults are : \n')
    print('Noise estimation : {}'.format(w[1]))
    for j in range(NBjointSet):
        print('Joint {}'.format(j))
        print('Mean: {}  --  '.format(w[j + 1]))
        print('Standard deviation : {}  --  '.format(w[NBjointSet + j + 1]))
        print('Amplitude : {}'.format(w[2 * NBjointSet + j + 1]))

    return gaussian_param_OPT
