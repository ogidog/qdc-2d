import os

import numpy as np

from read_write_joints.splitNodes_per_setID import splitNodes_per_setID
from read_write_joints.writeJoints import writeJoints
import workflow.workflow_config as wfc


def classify_fromGaussians(limits):
    if limits == -1:
        print('Only 1 jointset selected -- No need for classification')
        nodes_classif = wfc.nodes
        return nodes_classif

    # Classify jointSet
    print('Classification of joint set --> Started')
    wfc.nodes['setiD'] = []
    for i in range(len(wfc.nodes['iD'])):
        joint_orientation = wfc.nodes['ori_mean_deg'][i]
        for inter in range(len(limits) - 1):
            if joint_orientation >= limits[inter] and joint_orientation < limits[inter + 1]:
                wfc.nodes['setiD'].append(inter + 1)

        if joint_orientation >= limits[-1] or joint_orientation < limits[0]:
            wfc.nodes['setiD'].append(0)

    nodes_classif = wfc.nodes

    # Split nodes and write in OutPath
    output_file_template = wfc.template['OUTPUT'] + os.path.sep + "classif.txt"
    for set in range(len(limits)):
        out = output_file_template.replace('.', ('_{}classif.'.format(str(set))))
        split_nodes = splitNodes_per_setID(nodes_classif, set)
        split_matrice = writeJoints(split_nodes)
        np.savetxt(out, split_matrice, fmt="%d,%.10f,%.10f", delimiter=",")

    print('Classification of joint set --> DONE!');

    return nodes_classif
