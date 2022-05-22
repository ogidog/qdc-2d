import matplotlib.pyplot as plt
import numpy as np

from read_write_joints.readJoints import readJoints
from analysis.houghAnalysis.houghAnalysis import houghAnalysis
import workflow.lang as lang
import workflow.workflow_config as wfc


def run_hough(template):
    plt.close()

    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT')
        return

    nodes = readJoints(joint_file)
    nodes = houghAnalysis(nodes)
    print(lang.select_locale('Real spacing - Hough frame : {}\n'.format(np.mean(nodes['real_spacing_hough'])),
                             'Реальный интервал - Метод Хафа : {}\n'.format(np.mean(nodes['real_spacing_hough']))))

    wfc.hough_brief[lang.select_locale('Real spacing - Hough frame : {}\n'.format(np.mean(nodes['real_spacing_hough'])),
                                       'Реальный интервал - Метод Хафа : {}\n'.format(np.mean(nodes['real_spacing_hough'])))]

    return nodes
