import csv

import numpy as np

from read_write_joints.readJoints import readJoints


def run_hough(template):
    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT')
        return

    joints = np.array([])
    with open(joint_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            joints = np.append(joints, np.array(row))
    joints = np.array(np.split(joints, reader.line_num))
    nodes = readJoints(joints)
    # nodes = houghAnalysis(nodes);
    # fprintf('Real spacing - Hough frame : %f\n', mean((nodes.real_spacing_hough)))

    print()
