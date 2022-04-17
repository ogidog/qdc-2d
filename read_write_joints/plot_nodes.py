import matplotlib.pyplot as plt

def plot_nodes(nodes):
    for i in range(nodes['iD']):
        Xl = nodes['x'][i] # x-coordinate
        Yl = nodes['y'][i] # y-coordinate
        plot = plt.plot(Xl,Yl,'-','-b')

    plt.show()
