import os
import json
from matplotlib import pyplot as plt

# from TEMPLATES.run_function.hough import hough
from modules.volume import volume
from classify._withHistograms.classify_fromGaussians import classify_fromGaussians
from classify._withHistograms.find_jointSetLimits import find_jointSetLimits
from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram
import workflow.workflow_config as wfc
import utils.lang as lang
import utils.template as template


def classify_analyse_with_histograms(_template, nodes):
    wfc.template = _template
    wfc.nodes = nodes

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

    print(lang.select_locale('\n---------STARTING ANALYSIS---------', '\n---------ЗАПУСК АНАЛИЗА---------'))

    for j in range(len(files)):
        joint_file = wfc.template['OUTPUT'] + os.path.sep + files[j]
        print(lang.select_locale('\n--- File : {}\n', '\n--- Файл : {}\n').format(joint_file))
        set_iD = int(files[j].split('_')[-1].split("classif")[0])

        wfc.template['INPUT'] = joint_file

        # hough analyse
        # nodes = run_hough(wfc.template)
        #
        # # linear analyse
        # [frequency, spacing_real] = run_linear(wfc.template)
        #
        # # circular scanline
        # [intensity_estimator, density_estimator, traceLength_estimator] = run_circular(wfc.template)
        #
        # # persistance
        # persistance = run_persistence(wfc.template)
        #
        # # volume
        run_volume(wfc.template)
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


if __name__ == "__main__":
    _template = template.init()
    workflow_classify_Analyse_withHistograms(_template)
