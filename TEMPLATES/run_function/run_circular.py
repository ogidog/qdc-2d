from matplotlib import pyplot as plt

from analysis.circularScanline.circularScanline import circularScanline
from read_write_joints.readJoints import readJoints


def run_circular(template):
    plt.close()

    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT')
        return

    prompt = 'Number of horizontal circles? : '
    circles = input(prompt)

    nodes = readJoints(joint_file)
    circularScanline(nodes, int(circles))