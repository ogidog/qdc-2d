import numpy as np


def writeJoints(nodes):

    matrice = []
    for i in range(len(nodes['iD'])):
        id = nodes['iD'][i]* np.ones(np.size(nodes['x'][i], 0))
        #matrice = [matrice ; [id,nodes.x{i}, nodes.y{i}]];

    return matrice