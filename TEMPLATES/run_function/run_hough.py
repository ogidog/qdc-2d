import numpy as np

from read_write_joints.readJoints import readJoints
from houghAnalysis.houghAnalysis import houghAnalysis


def run_hough(template):
    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT')
        return

    nodes = readJoints(joint_file)
    nodes = houghAnalysis(nodes)
    print('Real spacing - Hough frame : {}\n'.format(np.mean(nodes['real_spacing_hough'])))
