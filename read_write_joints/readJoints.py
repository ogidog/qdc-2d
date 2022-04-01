import numpy as np


def readJoints(matrix_joints):
    nodes = {}
    iD = np.unique(matrix_joints[:, 0].astype(int))
    for i in range(len(iD)):
        row = matrix_joints[matrix_joints[:,0]==iD[i]] #all lines of iD i
        nodes[iD[i]]= iD[i]
        #nodes[x{i} = matrix_joints(row,2);
        #nodes.y{i} = matrix_joints(row,3);

    print()
