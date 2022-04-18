
def plot_nodes(nodes, plt):
    for i in range(len(nodes['iD'])):
        Xl = nodes['x'][i].flatten()  # x-coordinate
        Yl = nodes['y'][i].flatten()  # y-coordinate
        plt.plot(Xl, Yl, "b-")
