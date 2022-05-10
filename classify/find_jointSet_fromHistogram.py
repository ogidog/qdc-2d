import numpy as np
from matplotlib import pyplot as plt


def find_jointSet_fromHistogram(nodes):
    global theta_vector
    global theta_histogram
    theta_vector = [*range(0, 181, 2)]

    plt.figure(1)
    theta = nodes['ori_mean']
    #polarhistogram([theta;theta+pi],50);
    ax = plt.subplot(polar=True)
    #ax.bar(theta, height1, bottom=0.0, width=np.pi / N, alpha=0.5, edgecolor="black", align="edge")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.title.set_text('Rose diagram (°)')
    plt.show()

    pass

    # return gaussian_param_OPT
