import matplotlib.pyplot as plt
import numpy as np

from read_write_joints.polylines_to_lines import polylines_to_lines


def plot_inHoughFrame(nodes):
    # Create Hough matrix from nodes
    [nodes,*_] = polylines_to_lines(nodes)

    plt.figure(1)
    plt.title('Hough transform')
    plt.xlabel('Theta')
    plt.ylabel('r')
    plt.show(block=False)

    plt.figure(2)
    nodes['r'] = [*range(len(nodes['iD']))]
    for j in range(len(nodes['iD'])):
        x = nodes['line'][j][0]
        y = nodes['line'][j][2]
        nodes['r'][j] = np.abs(y*np.cos(np.radians(nodes['ori_mean_deg'][j])) - x*np.sin(np.radians(nodes['ori_mean_deg'][j])))
        plt.plot(nodes['ori_mean_deg'][j], nodes['r'][j], 'r.')
    plt.show(block=False)

    return nodes
