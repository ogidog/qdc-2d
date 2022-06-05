import os
import numpy as np

from modules.circular import circular
from modules.hough import hough
from modules.linear import linear
from modules.persistence import persistence
from modules.volume import volume
from modules.wavelet import wavelet

from utils.read_joints import read_joints
from utils.write_json import write_json
import utils.template as template
import utils.lang as lang
from analysis.mean_orientation import mean_orientation
from classify._withHistograms.classify_fromGaussians import classify_fromGaussians
from classify._withHistograms.find_jointSetLimits import find_jointSetLimits
from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram

def classify_analyse_with_histograms(joints_source: str = None):
    try:

        template.nodes = read_joints(joints_source)

        # -- Classification

        gaussianParams = find_jointSet_fromHistogram()
        limits = find_jointSetLimits(gaussianParams)
        classify_fromGaussians(limits)

        files = list(filter(lambda file: "classif" in file, os.listdir(template.config['OUTPUT'])))
        resume = {lang.select_locale('SetId', 'Номер набора'): [],
                  lang.select_locale("nbTraces", 'Кол-во линий'): [],
                  lang.select_locale('orientation_mean', 'Значение угла наклона (среднее)'): [],
                  lang.select_locale('orientation_min', 'Значение угла наклона (минимальное)'): [],
                  lang.select_locale('orientation_max', 'Значение угла наклона (максимальное)'): [],
                  lang.select_locale('length_mean', 'Длина линии (средняя)'): [],
                  lang.select_locale('length_min', 'Длина линии (минимальная)'): [],
                  lang.select_locale('length_max', 'Длина линии (максимальная)'): [],
                  lang.select_locale('spacing_mean_linearScanline', 'Средняя длина интервала - Линейная развертка'): [],
                  lang.select_locale('spacing_min_linearScanline',
                                     'Минимальная длина интервала - Линейная развертка'): [],
                  lang.select_locale('spacing_max_linearScanline',
                                     'Максимальная длина интервала - Линейная развертка'): [],
                  lang.select_locale('spacing_mean_houghAnalyse', 'Средняя длина интервала - Метод Хафа'): [],
                  lang.select_locale('spacing_min_houghAnalyse', 'Минимальная длина интервала - Метод Хафа'): [],
                  lang.select_locale('spacing_max_houghAnalyse', 'Максимальная длина интервала - Метод Хафа'): [],
                  lang.select_locale('persistence_mean', 'Коэффициент постоянства линий (среднее)'): [],
                  lang.select_locale('persistence_min', 'Коэффициент постоянства линий (минимальное)'): [],
                  lang.select_locale('persistence_max', 'Коэффициент постоянства линий (максимальный)'): [],
                  lang.select_locale('spacing_frequency', 'Частота интервалов'): [],
                  lang.select_locale('intensity_estimator', 'Оценка интенсивность линий'): [],
                  lang.select_locale('density_estimator', 'Оценка плотности линий'): [],
                  lang.select_locale('traceLength_estimator', 'Оценка длин линий'): []}

        print(lang.select_locale('\n---------STARTING ANALYSIS---------', '\n---------ЗАПУСК АНАЛИЗА---------'))

        for j in range(len(files)):
            joint_file = template.config['OUTPUT'] + os.path.sep + files[j]
            print(lang.select_locale('\n--- File : {}\n', '\n--- Файл : {}\n').format(joint_file))
            set_iD = int(files[j].split('_')[-1].split("classif")[0])

            template.config['INPUT'] = joint_file

            # hough analyse
            nodes = hough()

            # linear analyse
            [frequency, spacing_real] = linear()

            # circular scanline
            [intensity_estimator, density_estimator, traceLength_estimator] = circular()

            # persistance
            persistance = persistence()

            # volume
            volume()

            # wavelet
            wavelet()

            # -- summarize
            resume[lang.select_locale('SetId', 'Номер набора')].append(set_iD)
            resume[lang.select_locale('nbTraces', 'Кол-во линий')].append(len(nodes['iD']))
            orientations = mean_orientation(nodes)
            resume[lang.select_locale('orientation_mean', 'Значение угла наклона (среднее)')].append(
                orientations['MEAN'])
            resume[lang.select_locale('orientation_min', 'Значение угла наклона (минимальное)')].append(
                orientations['MIN'])
            resume[lang.select_locale('orientation_max', 'Значение угла наклона (максимальное)')].append(
                orientations['MAX'])
            resume[lang.select_locale('length_mean', 'Длина линии (средняя)')].append(np.mean(nodes['norm']))
            resume[lang.select_locale('length_min', 'Длина линии (минимальная)')].append(np.min(nodes['norm']))
            resume[lang.select_locale('length_max', 'Длина линии (максимальная)')].append(np.max(nodes['norm']))
            resume[lang.select_locale('spacing_mean_linearScanline',
                                      'Средняя длина интервала - Линейная развертка')].append(np.mean(spacing_real))
            resume[lang.select_locale('spacing_min_linearScanline',
                                      'Минимальная длина интервала - Линейная развертка')].append(np.min(spacing_real))
            resume[lang.select_locale('spacing_max_linearScanline',
                                      'Максимальная длина интервала - Линейная развертка')].append(np.max(spacing_real))
            resume[lang.select_locale('spacing_mean_houghAnalyse', 'Средняя длина интервала - Метод Хафа')].append(
                np.mean(nodes['real_spacing_hough']))
            resume[lang.select_locale('spacing_min_houghAnalyse', 'Минимальная длина интервала - Метод Хафа')].append(
                np.min(nodes['real_spacing_hough']))
            resume[lang.select_locale('spacing_max_houghAnalyse', 'Максимальная длина интервала - Метод Хафа')].append(
                np.max(nodes['real_spacing_hough']))
            resume[lang.select_locale('persistence_mean', 'Коэффициент постоянства линий (среднее)')].append(
                np.mean(persistance))
            resume[lang.select_locale('persistence_min', 'Коэффициент постоянства линий (минимальное)')].append(
                np.min(persistance))
            resume[lang.select_locale('persistence_max', 'Коэффициент постоянства линий (максимальный)')].append(
                np.max(persistance))
            resume[lang.select_locale('spacing_frequency', 'Частота интервалов')].append(frequency)
            resume[lang.select_locale('intensity_estimator', 'Оценка интенсивность линий')].append(intensity_estimator)
            resume[lang.select_locale('density_estimator', 'Оценка плотности линий')].append(density_estimator)
            resume[lang.select_locale('traceLength_estimator', 'Оценка длин линий')].append(traceLength_estimator)

            template.classif_joint_set_counter += 1

        template.classif_joint_set_counter = "common"
        write_json(resume, template.config['OUTPUT'])

    except Exception as exc:
        # TODO: log here
        print(exc.with_traceback())