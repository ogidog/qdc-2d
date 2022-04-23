
def plot_nodes(nodes, plt):
    for i in range(len(nodes['iD'])):
        Xl = nodes['x'][i]  # x-coordinate
        Yl = nodes['y'][i]  # y-coordinate
        plt.plot(Xl, Yl, "b-")
