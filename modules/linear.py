import os
import matplotlib.pyplot as plt
import numpy as np

from analysis.linearScanline.linearScanline import linearScanline
from utils.read_joints import read_joints
from utils.write_json import write_json
import utils.lang as lang
import utils.template as template


def linear():
    plt.close()

    print(lang.select_locale('Analyse with linear scanline','Анализ - Линейная развертка'))

    if not os.path.exists(template.config['LINEAR_OUTPUT']):
        os.makedirs(template.config['LINEAR_OUTPUT'])

    info_scanline = {}
    if 'NORTH' in template.config.keys():
        info_scanline['north'] = template.config['NORTH']
        print(lang.select_locale('North orientation given. Joints rotation',
                                 'Задана ориентация - Север. Поворот линий на заданный угол.'))
    else:
        info_scanline['north'] = 0

    nodes = read_joints()
    nodes['synthetic'] = template.config['SYNTHETIC']

    info_scanline['nbScan'] = 30

    [frequency, spacing_real, THETA] = linearScanline(nodes, info_scanline)

    print(lang.select_locale("Real spacing : {}", "Реальный интервал (среднее): {}").format(np.mean(spacing_real)))
    template.linear_brief[lang.select_locale('Real spacing', "Реальный интервал (среднее)")] = np.mean(spacing_real)

    print(lang.select_locale("Mean orientation : {}", "Угол наклона линии (среднее) : {}").format(
        np.mean(np.rad2deg(THETA))))
    template.linear_brief[lang.select_locale('Mean orientation', 'Угол наклона линии (среднее)')] = np.mean(
        np.mean(np.rad2deg(THETA)))

    print(lang.select_locale("Trace length : {}", "Длина линии (среднее) : {}").format(np.mean(nodes['norm'])))
    template.linear_brief[lang.select_locale('Trace length', 'Длина линии (среднее)')] = np.mean(nodes['norm'])

    write_json(template.linear_brief, template.config['LINEAR_OUTPUT'])

    return [frequency, spacing_real]
