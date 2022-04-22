import numpy as np
from shapely.geometry import LineString, Point, MultiLineString

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
    best_intersection_x = []
    best_intersection_y = []

    linesCoord = list(np.zeros((len(x_joint) - 1, 1)))
    for i in range(len(x_joint) - 1):
        linesCoord[i] = ((x_joint[i], y_joint[i]), (x_joint[i + 1], y_joint[i + 1]))
    jointLines = MultiLineString(linesCoord)

    for scan in range(scanline_iterations):
        # create random scanline
        theta_scanline = np.random.random() * 0.99 * np.pi
        random_scanline = create_scanline(xminmax, yminmax, theta_scanline)

        scanline = LineString([(random_scanline['Xsl'][0][0], random_scanline['Ysl'][0][0]),
                               (random_scanline['Xsl'][1][0], random_scanline['Ysl'][1][0])])
        intersection = jointLines.intersection(scanline)
        intersection_length = len(intersection.geoms)
        if intersection_length > nb_cross:
            nb_cross = intersection_length
            best_scanline = random_scanline

    return best_scanline
