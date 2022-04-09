import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from houghAnalysis.plot_inHoughFrame import plot_inHoughFrame


def houghAnalysis(nodes):
    plt.close()

    nodes = plot_inHoughFrame(nodes)
    [mu, sigma] = norm.fit(np.array(nodes['ori_mean_deg']).reshape(-1, 1))
    print('Gaussian distribution parameters for orientation: \n mu={} -- sigma={}\n'.format(mu, sigma))

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
    nodes['app_spacing_hough']  = app_spacing


    pass
