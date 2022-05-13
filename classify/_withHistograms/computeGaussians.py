import numpy as np
from scipy.stats import norm

def computeGaussians(jointset_info):
    gaussians = {}

    theta_vector = np.arange(0, 179, 2)
    NBjointSet = jointset_info['NBjointSet']
    gaussian_curves = np.zeros((90, NBjointSet))
    G_mean = jointset_info['G_mean']
    G_std = jointset_info['G_std']
    G_N = jointset_info['G_N']

    for joint in range(0, NBjointSet):
        H = np.zeros(90)
        histo1 = G_N[joint] * norm.pdf(theta_vector, G_mean[joint], G_std[joint])
        histo2 = G_N[joint] * norm.pdf(theta_vector - 180, G_mean[joint], G_std[joint])
        histo3 = G_N[joint] * norm.pdf(theta_vector + 180, G_mean[joint], G_std[joint])
        indice1 = np.where(histo1 > 0.0001)
        indice2 = np.where(histo2 > 0.0001)
        indice3 = np.where(histo3 > 0.0001)
        H[indice1] = histo1[indice1]
        H[indice2] = histo2[indice2]
        H[indice3] = histo3[indice3]
        gaussian_curves[:, joint] = H

    gaussians['curves'] = gaussian_curves
    gaussians['sum'] = np.sum(gaussian_curves, 1) + jointset_info['noise']

    return gaussians
