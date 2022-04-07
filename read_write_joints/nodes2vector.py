import numpy as np


def nodes2vector(nodes):
    vector = {}
    vector['ori'] = np.array(nodes['ori_mean']).flatten()
    vector['length_vector'] = np.array(nodes['norm']).flatten()
    vector['x'] = np.array(nodes['x']).flatten()
    vector['y'] = np.array(nodes['y']).flatten()

    return vector