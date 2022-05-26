import numpy as np


def nodes2vector(nodes):
    vector = {}
    vector['ori'] = np.array(nodes['ori_mean']).flatten()
    vector['length_vector'] = np.array(nodes['norm']).flatten()
    vector['x'] = nodes['x'].flatten()
    vector['y'] = nodes['y'].flatten()

    return vector