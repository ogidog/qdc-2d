from read_write_joints.splitNodes_per_setID import splitNodes_per_setID
from read_write_joints.writeJoints import writeJoints


def classify_fromGaussians(limits, nodes, outPath):
    if limits == -1:
        print('Only 1 jointset selected -- No need for classification')
        nodes_classif = nodes
        return nodes_classif

    # Classify jointSet
    print('Classification of joint set --> Started')
    nodes['setiD'] = []
    for i in range(len(nodes['iD'])):
        joint_orientation = nodes['ori_mean_deg'][i]
        for inter in range(len(limits) - 1):
            if joint_orientation >= limits[inter] and joint_orientation < limits[inter + 1]:
                nodes['setiD'].append(inter + 1)

        if joint_orientation >= limits[-1] or joint_orientation < limits[0]:
            nodes['setiD'].append(0)

    nodes['setiD'] = nodes['setiD'] + 1
    nodes_classif = nodes

    # Split nodes and write in OutPath
    for set in range(len(limits)):
        out = outPath.replace('.', ('_{}classif.'.format(str(set))))
        split_nodes = splitNodes_per_setID(nodes_classif, set)
        split_matrice = writeJoints(split_nodes)
        # writematrix(split_matrice, out)

    print('Classification of joint set --> DONE!');

    return nodes_classif
