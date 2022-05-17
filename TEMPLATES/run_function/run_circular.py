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

    if 'CIRCLES' in template.keys():
        circles = template['CIRCLES']
    else:
        prompt = 'Number of horizontal circles? : '
        circles = input(prompt)

    nodes = readJoints(joint_file)
    [intensity_estimator, density_estimator, traceLength_estimator] = circularScanline(nodes, int(circles))

    return [intensity_estimator, density_estimator, traceLength_estimator]
