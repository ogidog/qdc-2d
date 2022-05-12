import numpy as np

from matplotlib import pyplot as plt

from classify._withHistograms.computeGaussians import computeGaussians
from classify._withHistograms.jointSet_estimation_byUser import jointSet_estimation_byUser
from classify._withHistograms.smoothHisto import smoothHisto


def find_jointSet_fromHistogram(nodes):
    theta_vector = [*range(0, 181, 2)]

    plt.figure(1)
    theta = nodes['ori_mean']
    N = 50
    x = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    [y, _] = np.histogram(np.array([np.array(theta), np.array(theta) + np.pi]), N)
    ax = plt.subplot(polar=True)
    ax.bar(x, y, bottom=0.0, width=2 * np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    plt.show()

    plt.figure(2)
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_title('Estimated result')
    ax1.set_xlabel('Orientation (degrees)')
    ax1.set_ylabel('Counts')
    ax1.plot(theta_vector[:-1], nodes['oriHisto'], '--', color=[0.5, 0.5, 0], label="Raw data")  # plot tracelength
    ax1.set_xtick = np.arange(0, 190, 10)
    # Plot smoothed data
    theta_histogram_smoothed = smoothHisto(nodes['oriHisto'], 10)
    ax1.plot(theta_vector[:-1], theta_histogram_smoothed, '-', color=[1, 0, 0], label="Smoothed data")
    ax1.legend()

    # -- USER estimation
    gaussian_param_esti = jointSet_estimation_byUser()

    # Create Gaussian curves
    gaussians = computeGaussians(gaussian_param_esti)

    # Plot first estimation
    for curve in range(np.size(gaussians['curves'], axis=1)):
        plt.plot(np.array(theta_vector[:-1]), gaussians['curves'][:, curve].flatten())
    plt.plot(theta_vector[:-1], gaussians['sum'], linewidth=2)

    # -- Optimization
    theta_histogram = nodes['oriHisto']
    w0 = [gaussian_param_esti['noise']]
    w0.extend(gaussian_param_esti['G_mean'])
    w0.extend(gaussian_param_esti['G_std'])
    w0.extend(gaussian_param_esti['G_N'])

    #[w,~] = fminunc( @(x) minimizeFunction(x), w0);

    plt.show()

    # return gaussian_param_OPT
