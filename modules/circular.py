import os
from matplotlib import pyplot as plt

from analysis.circularScanline.circularScanline import circularScanline
from utils.read_joints import read_joints
import utils.lang as lang
import utils.template as template
from utils.write_json import write_json


def circular():

    plt.close()

    print(lang.select_locale('Analyse with circular scanline','Анализ - Метод сканирующих окружностей'))
    template.circular_brief[lang.select_locale('Method', 'Модуль')] = lang.select_locale('Analyse with circular scanline','Анализ - Метод сканирующих окружностей')

    if 'CIRCLES' in template.config.keys():
        circles = template.config['CIRCLES']
    else:
        prompt = lang.select_locale('Number of horizontal circles? :', 'Количество окружностей по горизонтали? : '),
        circles = input(prompt)

    nodes = read_joints()
    [intensity_estimator, density_estimator, traceLength_estimator] = circularScanline(nodes, int(circles))

    write_json(template.circular_brief, template.config['CIRCULAR_OUTPUT'])

    return [intensity_estimator, density_estimator, traceLength_estimator]
