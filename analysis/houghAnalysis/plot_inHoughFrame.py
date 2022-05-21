import matplotlib.pyplot as plt
import numpy as np

from read_write_joints.polylines_to_lines import polylines_to_lines


def plot_inHoughFrame(nodes):

    plt.figure(1)
    # Create Hough matrix from nodes
    [nodes,*_] = polylines_to_lines(nodes)
    # plt.title('Hough transform')
    plt.title('Трансформация Хафа')
    plt.xlabel('Theta')
    plt.ylabel('r')
    plt.show(block=False)

    plt.figure(2)
    plt.subplots(constrained_layout=True)
    nodes['r'] = [*range(len(nodes['iD']))]
    for j in range(len(nodes['iD'])):
        x = nodes['line'][j][0]
        y = nodes['line'][j][2]
        nodes['r'][j] = np.abs(y*np.cos(np.radians(nodes['ori_mean_deg'][j])) - x*np.sin(np.radians(nodes['ori_mean_deg'][j])))
        plt.plot(nodes['ori_mean_deg'][j], nodes['r'][j], 'r.')
        # plt.title("Distribution of the orientation mean degree")
        plt.title("Распределение средних значений угла наклона")
    plt.show(block=False)

    return nodes
