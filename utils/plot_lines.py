from matplotlib import pyplot as plt


def plot_lines(nodes):
    if 'line' in nodes.keys():
        for i in range(len(nodes['iD'])):
            Xl = nodes['line'][i][0:2]  # x-coordinate
            Yl = nodes['line'][i][2:4]  # y-coordinate
            plt.plot(Xl, Yl, 'b-')
    else:
        print('No lines to plot ! ')
