import os.path

import matplotlib.pyplot as plt
import numpy as np

from utils.read_joints import read_joints
from analysis.houghAnalysis.houghAnalysis import houghAnalysis
from utils.write_json import write_json
import utils.lang as lang
import utils.template as template


def hough(joints_source: str = None):
    plt.close()

    print(lang.select_locale('Analyse with Hough frame', 'Анализ - Метод Хафа'))
    template.hough_brief[lang.select_locale('Method', 'Модуль')] = lang.select_locale('Analyse with Hough frame', 'Анализ - Метод Хафа')

    nodes = read_joints(joints_source)
    nodes = houghAnalysis(nodes)

    print(lang.select_locale('Real spacing - Hough frame : {}\n', 'Реальный интервал - Метод Хафа : {}\n').format(
        np.mean(nodes['real_spacing_hough'])))

    template.hough_brief[lang.select_locale('Real spacing - Hough frame', 'Реальный интервал - Метод Хафа')] = np.mean(
        nodes['real_spacing_hough'])

    write_json(template.hough_brief, template.config['HOUGH_OUTPUT'])

    return nodes
