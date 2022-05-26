import os
import matplotlib.pyplot as plt
import numpy as np

from analysis.linearScanline.linearScanline import linearScanline
from utils.readJoints import readJoints
from utils.write_json import write_json
import utils.lang as lang
import utils.template as template


def linear(template):
    plt.close()

    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT (mandatory)')
        return

    if not os.path.exists(template.config['LINEAR_OUTPUT']):
        os.makedirs(template.config['LINEAR_OUTPUT'])

    info_scanline = {}
    if 'NORTH' in template.keys():
        info_scanline['north'] = template['NORTH']
        print(lang.select_locale('North orientation given. Joints rotation',
                                 'Задана ориентация - Север. Поворот линий на заданный угол.'))
    else:
        info_scanline['north'] = 0

    nodes = readJoints(joint_file)
    nodes['synthetic'] = template['SYNTHETIC']

    info_scanline['nbScan'] = 30

    [frequency, spacing_real, THETA] = linearScanline(nodes, info_scanline)

    print(lang.select_locale("Real spacing : {}", "Реальный интервал (среднее): {}").format(np.mean(spacing_real)))
    wfc.linear_brief[lang.select_locale('Real spacing', "Реальный интервал (среднее)")] = np.mean(spacing_real)

    print(lang.select_locale("Mean orientation : {}", "Угол наклона линии (среднее) : {}").format(
        np.mean(np.rad2deg(THETA))))
    wfc.linear_brief[lang.select_locale('Mean orientation', 'Угол наклона линии (среднее)')] = np.mean(
        np.mean(np.rad2deg(THETA)))

    print(lang.select_locale("Trace length : {}", "Длина линии (среднее) : {}").format(np.mean(nodes['norm'])))
    wfc.linear_brief[lang.select_locale('Trace length', 'Длина линии (среднее)')] = np.mean(nodes['norm'])

    write_json(wfc.linear_brief,
               template.config['LINEAR_OUTPUT'] + os.path.sep + "brief_" + str(wfc.classif_joint_set_counter) + ".json")

    return [frequency, spacing_real]
