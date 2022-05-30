import os

from matplotlib import pyplot as plt

from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram
from modules.circular import circular
from modules.hough import hough
from modules.linear import linear
from modules.persistence import persistence
from modules.volume import volume
from modules.wavelet import wavelet
import utils.template as template
from utils.read_joints import read_joints
import utils.lang as lang


def classify_analyse_with_histograms(config_vars_json: str = None, nodes_source: str = None):
    try:
        template.config = template.init(config_vars_json)
        template.nodes = read_joints(nodes_source)

        # -- Classification

        plt.close()

        if not os.path.exists(template.config['OPTIMIZATION_OUTPUT']):
             os.makedirs(template.config['OPTIMIZATION_OUTPUT'])

        gaussianParams = find_jointSet_fromHistogram()
        # limits = find_jointSetLimits(gaussianParams)
        # classify_fromGaussians(limits)
        #
        # files = list(filter(lambda file: "classif" in file, os.listdir(template.config['OUTPUT'])))
        # resume = {lang.select_locale('SetId', 'Номер'): [],
        #           lang.select_locale("nbTraces", 'Кол-во линий'): [],
        #           lang.select_locale('orientation_mean', 'Среднее значение угла наклона'): [],
        #           lang.select_locale('orientation_min', 'Минимальное значение угла наклона'): [],
        #           lang.select_locale('orientation_max', 'Максимальное значение угла наклона'): [],
        #           lang.select_locale('length_mean', 'Средняя длина линии'): [],
        #           lang.select_locale('length_min', 'Минимальная длина линии'): [],
        #           lang.select_locale('length_max', 'Максимальная длина линии'): [],
        #           lang.select_locale('spacing_mean_linearScanline', 'Средняя длина интервала - Линейная развертка'): [],
        #           lang.select_locale('spacing_min_linearScanline', 'Минимальная длина интервала - Линейная развертка'): [],
        #           lang.select_locale('spacing_max_linearScanline', 'Максимальная длина интервала - Линейная развертка'): [],
        #           lang.select_locale('spacing_mean_houghAnalyse', 'Средняя длина интервала - Метод Хафа'): [],
        #           lang.select_locale('spacing_min_houghAnalyse', 'Минимальная длина интервала - Метод Хафа'): [],
        #           lang.select_locale('spacing_max_houghAnalyse', 'Максимальная длина интервала - Метод Хафа'): [],
        #           lang.select_locale('persistence_mean', 'Средний коэффициент постоянства линий'): [],
        #           lang.select_locale('persistence_min', 'Минимальный коэффициент постоянства линий'): [],
        #           lang.select_locale('persistence_max', 'Максимальный коэффициент постоянства линий'): [],
        #           lang.select_locale('spacing_frequency', 'Частота интервалов'): [],
        #           lang.select_locale('intensity_estimator', 'Оценка интенсивность линий'): [],
        #           lang.select_locale('density_estimator', 'Оценка плотности линий'): [],
        #           lang.select_locale('traceLength_estimator', 'Оценка длин линий'): []}
        #
        # print(lang.select_locale('\n---------STARTING ANALYSIS---------', '\n---------ЗАПУСК АНАЛИЗА---------'))

        # for j in range(len(files)):
        #     joint_file = template.config['OUTPUT'] + os.path.sep + files[j]
        #     print(lang.select_locale('\n--- File : {}\n', '\n--- Файл : {}\n').format(joint_file))
        #     set_iD = int(files[j].split('_')[-1].split("classif")[0])
        #
        #     template.config['INPUT'] = joint_file

            # hough analyse
            # nodes = hough()
            #
            # # linear analyse
            # [frequency, spacing_real] = run_linear(template.config)
            #
            # # circular scanline
            # [intensity_estimator, density_estimator, traceLength_estimator] = run_circular(template.config)
            #
            # # persistance
            # persistance = run_persistence(template.config)
            #
            # # volume
            # run_volume(template.config)
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

            # template.classif_joint_set_counter += 1

        # summarizeTable = json.dumps(resume)

        # return summarizeTable, files

        pass

    except Exception as exc:
        # TODO: log here
        print(exc)


def main(config_vars_json):

    try:

        template.config = template.init(config_vars_json)

        if template.config['STEP'] == 'HELP' or template.config['STEP'] == '-h':
            f = open('help.txt', mode="r")
            while True:
                line = f.readline()
                if line == "":
                    f.close()
                    break
                print(line)

        # -- Step 2 : Classify joints
        if template.config['STEP'] == 2:
            print('STEP 2 : Classify joints')
            if 'METHOD' in template.config.keys():
                if template.config.METHOD == "hough":
                    print('Classify with Hough')
                    # UI_classif_withHough()
                elif template.config['METHOD'] == "histo":
                    print('Classify with oriention histograms')
                    # UI_classif_withGauss()
                else:
                    print('Available method for STEP 2 : histo or hough')
                    return
            else:
                print('No METHOD:histo/hough')
                return

        # -- Step 3 : Analysis 1 jointset
        if int(template.config['STEP']) == 3:
            # print('STEP 3 : Analyse jointset')
            print('Шаг 3 : Анализ набора линий\n')
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "hough":
                    # print('Analyse with Hough frame')
                    print('Анализ - Метод Хафа')
                    hough()
                    return
                elif template.config['METHOD'] == "linear":
                    # print('Analyse with linear scanline')
                    print('Анализ - Линейная разверткой\n')
                    linear()
                    return
                elif template.config['METHOD'] == "persistence":
                    print('Analyse the persistence')
                    persistence()
                    return
                elif template.config['METHOD'] == "wavelet":
                    print('Analyse spacing with wavelet transform')
                    wavelet()
                    return
                elif template.config['METHOD'] == "circular":
                    print('Analyse with circular scanline')
                    circular()
                    return
                elif template.config['METHOD'] == "parallelLinear":
                    pass
                    # parallelLinear()
            else:
                print(
                    'Available method for STEP 3 : hough or linear or parallelLinear or circular or wavelet or persistence')
                return
        else:
            print('No METHOD;hough/linear/persistence')

        # -- Step 4 : Analysis all jointsets
        if int(template.config['STEP']) == 4:
            print('STEP 4 : Characterization of the jointing degree ')
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "circular":
                    print('Analyse circular scanline')
                    circular()
                    return
                elif template.config['METHOD'] == "volume":
                    print('Analyse block volume and volume joint count')
                    volume()
                    return
            else:
                print('Available method for STEP 4 : circular or volume')
                return
        else:
            print('No METHOD;circular/volume')

    except ValueError:
        print(ValueError)


if __name__ == "__main__":
    # TODO: For tests only
    #
    config_vars_json = '{"jNAME":["j1","j2","j3"],"jORIENTATION":[10.0,40.0,100.0],"jSPACING":[5.0,10.0,10.0],"G_MEAN":[5.0,1.0],"G_STD":[7.0,9.0],"G_N":[69.0,22.0],"SYNTHETIC":0,"STEP":"3","METHOD":"hough","THETA":10.0,"SCALE":10.0,"COVER":0.9,"CIRCLES":5,"SQUARES":5,"SCANS":2.0,"G_NOISE":2,"DX":2.0,"DY":2.0}'
    ######################

    classify_analyse_with_histograms(config_vars_json)
    # main()
