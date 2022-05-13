import numpy as np
from scipy.stats import norm

def minimizeFunction(w, theta_histogram):

    theta_vector = np.arange(0, 179, 2)

    NBjointSet = int(np.floor(len(w) / 3))
    histo_distribution_joint = np.zeros((90, NBjointSet))
    for joint in range(NBjointSet):
        H = np.zeros(90)
        histo1 = w[1 + 2 * NBjointSet + joint] * norm.pdf(theta_vector, w[1 + joint], w[1 + NBjointSet + joint])
        histo2 = w[1 + 2 * NBjointSet + joint] * norm.pdf(theta_vector - 180, w[1 + joint], w[1 + NBjointSet + joint])
        histo3 = w[1 + 2 * NBjointSet + joint] * norm.pdf(theta_vector + 180, w[1 + joint], w[1 + NBjointSet + joint])
        indice1 = np.where(histo1 > 0.0001)
        indice2 = np.where(histo2 > 0.0001)
        indice3 = np.where(histo3 > 0.0001)
        H[indice1] = histo1[indice1]
        H[indice2] = histo2[indice2]
        H[indice3] = histo3[indice3]
        histo_distribution_joint[:, joint] = H

    gaussian_sum = np.sum(histo_distribution_joint, 1) + w[0]
    gaussian_std = (theta_histogram - gaussian_sum) ** 2
    value2minimize = np.sum(gaussian_std) / 100000  # value to minimize

    return value2minimize
