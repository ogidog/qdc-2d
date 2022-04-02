import numpy as np
import cmath


def readJoints(matrix_joints):
    iD = np.unique(matrix_joints[:, 0])
    nodes = dict([('iD', np.zeros((len(iD), 1), dtype=np.float64)), ('x', np.zeros((len(iD), 2), dtype=np.float64)),
                  ('y', np.zeros((len(iD), 2), dtype=np.float64))])

    for i in range(len(iD)):
        row = np.where(matrix_joints[:, 0] == iD[i])  # all lines of iD i
        nodes['iD'][i] = iD[i]
        nodes['x'][i] = matrix_joints[row, 1]
        nodes['y'][i] = matrix_joints[row, 2]

        dx = np.diff(nodes['x'][i])[0]  # x-dimension of segment
        dy = np.diff(nodes['y'][i])[0]  # y-dimension of segment
        [rho, theta] = cmath.polar(complex(dx, dy))  # polar representation of incremental segment

        if theta < 0:
            theta = np.pi + theta
        elif np.pi / 2 >= theta >= 0:
            theta = np.pi / 2 - theta
        elif theta > np.pi / 2:
            theta = 3 * np.pi / 2 - theta

        pass

    print()
