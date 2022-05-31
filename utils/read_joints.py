import numpy as np
import cmath

import utils.template as template


def read_joints(joints_source: str = None):
    matrix_joints = np.array([])
    if joints_source:
        reader = joints_source.decode()
    else:
        f = open(template.config['INPUT'], 'r')
        reader = f.read()

    reader = reader.strip()[:-1].replace("\n", "").replace("\r", "").split(";")
    for row in reader:
        matrix_joints = np.append(matrix_joints, np.array(row.split(","), dtype=np.float64))
    matrix_joints = np.array(np.split(matrix_joints, len(reader)))

    iD = np.unique(matrix_joints[:, 0])
    nodes = dict([
        ('iD', np.array([*range(len(iD))])),
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
        nodes['iD'][i] = iD[i]
        nodes['x'][i] = matrix_joints[row, 1].flatten()
        nodes['y'][i] = matrix_joints[row, 2].flatten()

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
        nodes['oriHisto'] = N

    nodes['x'] = np.array(nodes['x'])
    nodes['y'] = np.array(nodes['y'])

    return nodes
