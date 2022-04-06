import numpy as np
import cmath

from utils import test_dict


def readJoints(matrix_joints):
    iD = np.unique(matrix_joints[:, 0])
    nodes = dict([
        ('iD', [*range(len(iD))]),
        ('x', [*range(len(iD))]),
        ('y', [*range(len(iD))]),
        ('nseg', [*range(len(iD))]),
        ('norm', [*range(len(iD))]),
        ('theta', [*range(len(iD))]),
        ('wi', [*range(len(iD))]),
        ('ori_w', [*range(len(iD))]),
        ('ori_mean', [*range(len(iD))]),
        ('ori_mean_deg', [*range(len(iD))])
    ])

    edges = [*range(0, 182, 2)]
    for i in range(len(iD)):
        row = np.where(matrix_joints[:, 0] == iD[i])  # all lines of iD i
        nodes['iD'][i] = [iD[i]]
        nodes['x'][i] = matrix_joints[row, 1]
        nodes['y'][i] = matrix_joints[row, 2]

        dx = np.diff(nodes['x'][i])  # x-dimension of segment
        dy = np.diff(nodes['y'][i])  # y-dimension of segment
        tmp_complex_arr = np.array([complex(dx[i], dy[i]) for i in range(len(dx))])
        [rho, theta] = np.array([cmath.polar(tmp_complex_arr[i]) for i in
                                 range(len(tmp_complex_arr))]).T  # polar representation of incremental segment

        theta[theta < 0] = np.pi + theta[theta < 0]
        theta[theta <= np.pi / 2] = np.pi / 2 - theta[theta <= np.pi / 2]
        theta[theta > np.pi / 2] = 3 * np.pi / 2 - theta[theta > np.pi / 2]

        nodes['nseg'][i] = len(dx)  # number of segments
        nodes['norm'][i] = np.sum(rho)  # norm of the sum of segments (trace length)

        nodes['theta'][i] = theta  # orientation of segments
        nodes['wi'][i] = rho / sum(rho)  # weight for segments
        nodes['ori_w'][i] = theta * nodes['wi'][i]
        nodes['ori_mean'][i] = sum(nodes['ori_w'][i]) / sum(nodes['wi'][i])
        nodes['ori_mean_deg'][i] = np.rad2deg(nodes['ori_mean'][i])
        [N, _] = np.histogram(nodes['ori_mean_deg'][0:(i + 1)], edges)
        nodes['oriHisto'] = N.reshape(-1, 1);

    del row

    # TODO: test
    # test_dict("D:\\Temp\\-QDC-2D-test\\nodes.mat", nodes, "nodes")

    return nodes
