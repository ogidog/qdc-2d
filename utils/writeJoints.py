import numpy as np


def writeJoints(nodes):
    id = (nodes['iD'][0] * np.ones(np.size(nodes['x'][0], 0))).astype("int")
    matrice = np.hstack((id.reshape(-1, 1), nodes['x'][0].reshape(-1, 1), nodes['y'][0].reshape(-1, 1)))
    for i in range(1, len(nodes['iD'])):
        id = (nodes['iD'][i] * np.ones(np.size(nodes['x'][i], 0))).astype("int")
        matrice = np.vstack(
            (matrice, np.hstack((id.reshape(-1, 1), nodes['x'][i].reshape(-1, 1), nodes['y'][i].reshape(-1, 1)))))

    return matrice
