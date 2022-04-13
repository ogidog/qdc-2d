import numpy as np

from analysis.linearScanline.create_scanline import create_scanline
from read_write_joints.nodes2vector import nodes2vector


def find_best_scanline(nodes, scanline_iterations):
    vector = nodes2vector(nodes)
    x_joint = vector['x']
    y_joint = vector['y']
    # get trace extents
    xminmax = np.append([np.min(vector['x'])], np.max(vector['x']))
    yminmax = np.append([np.min(vector['y'])], np.max(vector['y']))

    nb_cross = 0
    best_scanline = 0

    for scan in range(scanline_iterations):
        # create random scanline
        theta_scanline = np.random.random() * 0.99 * np.pi
        random_scanline = create_scanline(xminmax, yminmax, theta_scanline)

    pass
