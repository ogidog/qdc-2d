import os
import numpy as np
import json
from matplotlib import pyplot as plt

from TEMPLATES.run_function.run_circular import run_circular
from TEMPLATES.run_function.run_hough import run_hough
from TEMPLATES.run_function.run_linear import run_linear
from TEMPLATES.run_function.run_persistence import run_persistence
from TEMPLATES.run_function.run_volume import run_volume
from TEMPLATES.run_function.run_wavelet import run_wavelet
from analysis.mean_orientation import mean_orientation
from classify._withHistograms.classify_fromGaussians import classify_fromGaussians
from classify._withHistograms.find_jointSetLimits import find_jointSetLimits
from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram
from read_write_joints.readJoints import readJoints
from read_write_joints.read_template_file import read_template_file
import workflow.workflow_config as wfc
import workflow.lang as lang


def workflow_classify_Analyse_withHistograms(template_file):
    wfc.template = read_template_file(template_file)
    wfc.nodes = readJoints(wfc.template['INPUT'])

    plt.close()

    # -- Classification

    if not os.path.exists(wfc.template['OPTIMIZATION_OUTPUT']):
        os.makedirs(wfc.template['OPTIMIZATION_OUTPUT'])

    gaussianParams = find_jointSet_fromHistogram()
    limits = find_jointSetLimits(gaussianParams)
    classify_fromGaussians(limits)

    files = list(filter(lambda file: "classif" in file, os.listdir(wfc.template['OUTPUT'])))
    resume = {lang.select_locale('SetId', 'Номер'): [],
              lang.select_locale("nbTraces", 'Кол-во линий'): [],
              lang.select_locale('orientation_mean', 'Среднее значение угла наклона'): [],
              lang.select_locale('orientation_min', 'Минимальное значение угла наклона'): [],
              lang.select_locale('orientation_max', 'Максимальное значение угла наклона'): [],
              lang.select_locale('length_mean', 'Средняя длина линии'): [],
              lang.select_locale('length_min', 'Минимальная длина линии'): [],
              lang.select_locale('length_max', 'Максимальная длина линии'): [],
              lang.select_locale('spacing_mean_linearScanline', 'Средняя длина интервала - Линейная развертка'): [],
              lang.select_locale('spacing_min_linearScanline', 'Минимальная длина интервала - Линейная развертка'): [],
              lang.select_locale('spacing_max_linearScanline', 'Максимальная длина интервала - Линейная развертка'): [],
              lang.select_locale('spacing_mean_houghAnalyse', 'Средняя длина интервала - Метод Хафа'): [],
              lang.select_locale('spacing_min_houghAnalyse', 'Минимальная длина интервала - Метод Хафа'): [],
              lang.select_locale('spacing_max_houghAnalyse', 'Максимальная длина интервала - Метод Хафа'): [],
              lang.select_locale('persistence_mean', 'Средний коэффициент постоянства линий'): [],
              lang.select_locale('persistence_min', 'Минимальный коэффициент постоянства линий'): [],
              lang.select_locale('persistence_max', 'Максимальный коэффициент постоянства линий'): [],
              lang.select_locale('spacing_frequency', 'Частота интервалов'): [],
              lang.select_locale('intensity_estimator', 'Оценка интенсивность линий'): [],
              lang.select_locale('density_estimator', 'Оценка плотности линий'): [],
              lang.select_locale('traceLength_estimator', 'Оценка длин линий'): []}

    print(lang.select_locale('\n---------STARTING ANALYSIS---------\n', '\n---------ЗАПУСК АНАЛИЗА---------\n'))

    for j in range(len(files)):
        joint_file = wfc.template['OUTPUT'] + os.path.sep + files[j]
        print(lang.select_locale('--- File : {}'.format(joint_file), '--- Файл : {}'.format(joint_file)))
        set_iD = int(files[j].split('_')[-1].split("classif")[0])

        wfc.template['INPUT'] = joint_file

        # hough analyse
        nodes = run_hough(wfc.template)
        #
        # # linear analyse
        # [frequency, spacing_real] = run_linear(template)
        #
        # # circular scanline
        # [intensity_estimator, density_estimator, traceLength_estimator] = run_circular(template)
        #
        # # persistance
        # persistance = run_persistence(template)
        #
        # # volume
        # run_volume(template)
        #
        # # wavelet
        # run_wavelet(template)

        # -- summarize
        # resume['SetId'].append(set_iD)
        # resume['nbTraces'].append(len(nodes['iD']))
        # orientations = mean_orientation(nodes)
        # resume['orientation_mean'].append(orientations['MEAN'])
        # resume['orientation_min'].append(orientations['MIN'])
        # resume['orientation_max'].append(orientations['MAX'])
        # resume['length_mean'].append(np.mean(nodes['norm']))
        # resume['length_min'].append(np.min(nodes['norm']))
        # resume['length_max'].append(np.max(nodes['norm']))
        # resume['spacing_mean_linearScanline'].append(np.mean(spacing_real))
        # resume['spacing_min_linearScanline'].append(np.min(spacing_real))
        # resume['spacing_max_linearScanline'].append(np.max(spacing_real))
        # resume['spacing_mean_houghAnalyse'].append(np.mean(nodes['real_spacing_hough']))
        # resume['spacing_min_houghAnalyse'].append(np.min(nodes['real_spacing_hough']))
        # resume['spacing_max_houghAnalyse'].append(np.max(nodes['real_spacing_hough']))
        # resume['persistence_mean'].append(np.mean(persistance))
        # resume['persistence_min'].append(np.min(persistance))
        # resume['persistence_max'].append(np.max(persistance))
        # resume['spacing_frequency'].append(frequency)
        # resume['intensity_estimator'].append(intensity_estimator)
        # resume['density_estimator'].append(density_estimator)
        # resume['traceLength_estimator'].append(traceLength_estimator)

        wfc.classif_joint_set_counter += 1

    summarizeTable = json.dumps(resume)

    return summarizeTable, files


# def main(inputFile='D:\intellij-idea-workspace\qdc-2d\TEMPLATES\examples\createdJoints1.txt',
#          outputFolder='D:\intellij-idea-workspace\qdc-2d\TEMPLATES\examples\classif.txt',
#          template_file='D:\intellij-idea-workspace\qdc-2d\TEMPLATE.txt'):

def main(template_file='D:\intellij-idea-workspace\qdc-2d\TEMPLATE.txt'):
    workflow_classify_Analyse_withHistograms(template_file)


if __name__ == "__main__":
    main()
