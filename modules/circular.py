import os
from matplotlib import pyplot as plt

from analysis.circularScanline.circularScanline import circularScanline
from utils.read_joints import read_joints
import utils.lang as lang
import utils.template as template
from utils.write_json import write_json


def circular(template):
    plt.close()

    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT')
        return

    if 'CIRCLES' in template.keys():
        circles = template['CIRCLES']
    else:
        prompt = lang.select_locale('Number of horizontal circles? :', 'Количество окружностей по горизонтали? : '),
        circles = input(prompt)

    if not os.path.exists(template['CIRCULAR_OUTPUT']):
        os.makedirs(template['CIRCULAR_OUTPUT'])

    nodes = read_joints(joint_file)
    [intensity_estimator, density_estimator, traceLength_estimator] = circularScanline(nodes, int(circles))

    write_json(wfc.circular_brief, template['CIRCULAR_OUTPUT'] + os.path.sep + "brief_" + str(wfc.classif_joint_set_counter) + ".json")

    return [intensity_estimator, density_estimator, traceLength_estimator]
