import os.path

import matplotlib.pyplot as plt
import numpy as np

from utils.readJoints import readJoints
from analysis.houghAnalysis.houghAnalysis import houghAnalysis
from utils.write_json import write_json
import utils.lang as lang
import utils.template as template


def hough():
    plt.close()

    if 'INPUT' in template.config.keys():
        joint_file = template.config['INPUT']
    else:
        print('Missing arguments : INPUT')
        return

    if not os.path.exists(template.config['HOUGH_OUTPUT']):
        os.makedirs(template.config['HOUGH_OUTPUT'])

    nodes = readJoints(joint_file)
    nodes = houghAnalysis(nodes)

    print(lang.select_locale('Real spacing - Hough frame : {}\n', 'Реальный интервал - Метод Хафа : {}\n').format(
        np.mean(nodes['real_spacing_hough'])))

    template.hough_brief[lang.select_locale('Real spacing - Hough frame', 'Реальный интервал - Метод Хафа')] = np.mean(
        nodes['real_spacing_hough'])
    write_json(template.hough_brief, template.config['HOUGH_OUTPUT'] + os.path.sep + "brief_" + str(
        template.classif_joint_set_counter) + ".json")

    return nodes
