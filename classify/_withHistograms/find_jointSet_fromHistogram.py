import numpy as np

from matplotlib import pyplot as plt

from classify._withHistograms.jointSet_estimation_byUser import jointSet_estimation_byUser
from classify._withHistograms.smoothHisto import smoothHisto


def find_jointSet_fromHistogram(nodes):
    global theta_vector
    global theta_histogram
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

    plt.show()
    pass

    # return gaussian_param_OPT
