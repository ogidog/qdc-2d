import matplotlib.pyplot as plt
from read_write_joints.polylines_to_lines import polylines_to_lines


def plot_inHoughFrame(nodes):
    # Create Hough matrix from nodes
    [nodes, _] = polylines_to_lines(nodes)

    plt.title('Hough transform')
    plt.xlabel('Theta')
    plt.ylabel('r')

    plt.show()
