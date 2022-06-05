import os

from classify._withHistograms.classify_analyse_with_histograms import classify_analyse_with_histograms
from modules.circular import circular
from modules.hough import hough
from modules.linear import linear
from modules.parallel_linear import parallel_linear
from modules.persistence import persistence
from modules.volume import volume
from modules.wavelet import wavelet
import utils.template as template
import utils.lang as lang


def main(config_vars_json: str = None, joints_source: str = None, user_id: str = None, task_id: str = None):
    try:

        template.config = template.init_config(config_vars_json)
        if (user_id and task_id):
            root_dir = template.config['OUTPUT']
            output_keys = filter(lambda key: 'OUTPUT' in key and 'TYPE' not in key, template.config.keys())
            for key in output_keys:
                template.config[key] = template.config[key].replace(root_dir,
                                                                    root_dir
                                                                    + os.path.sep
                                                                    + str(user_id)
                                                                    + os.path.sep
                                                                    + str(task_id))

        # -- Step 2 : Classify joints
        if template.config['STEP'] == 2:
            print(lang.select_locale('\n--- Classify joints ---\n', '\n--- Классификация линий ---\n'))
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "hough":
                    print(lang.select_locale('Classify with Hough', 'Классификация линий - Метод Хафа'))
                    # UI_classif_withHough()
                elif template.config['METHOD'] == "histo":
                    print(lang.select_locale('Classify with Hough', 'Классификация линий - Метод гистограмм'))
                    classify_analyse_with_histograms(joints_source)
                    return
                else:
                    print(lang.select_locale('Available method : histo or hough',
                                             'Доступные значения для параметра METHOD: histo или hough'))
                    return
            else:
                print(lang.select_locale('No METHOD:histo/hough', 'Не задан параметр METHOD: (histo или hough)'))
                return

        # -- Step 3 : Analysis 1 jointset
        if int(template.config['STEP']) == 3:
            print(lang.select_locale('\n--- Analysis only jointset ---\n', '\n--- Анализ одного набора линий ---\n'))
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "hough":
                    hough(joints_source)
                    return
                elif template.config['METHOD'] == "linear":
                    linear(joints_source)
                    return
                elif template.config['METHOD'] == "persistence":
                    persistence(joints_source)
                    return
                elif template.config['METHOD'] == "wavelet":
                    wavelet(joints_source)
                    return
                elif template.config['METHOD'] == "circular":
                    circular(joints_source)
                    return
                elif template.config['METHOD'] == "parallelLinear":
                    parallel_linear(joints_source)
                    return
            else:
                print(lang.select_locale(
                    'Available method : hough or linear or parallelLinear or circular or wavelet or persistence',
                    'Доступные значения для параметра METHOD: hough, linear, parallelLinear, circular, wavelet или persistence'))
                return
        else:
            print('No METHOD;hough/linear/persistence',
                  'Не задан параметр METHOD: (hough, linear, parallelLinear, circular, wavelet или persistence)')
            return

        # -- Step 4 : Analysis all jointsets
        if int(template.config['STEP']) == 4:
            print(lang.select_locale('\n--- Characterization of the jointing degree ---\n',
                                     '\n--- Характеристика степени соединенности линий ---\n'))
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "circular":
                    circular()
                    return
                elif template.config['METHOD'] == "volume":
                    volume()
                    return
            else:
                print(lang.select_locale('Available method : circular or volume',
                                         'Доступные значения для параметра METHOD: circular или volume'))
                return
        else:
            print(lang.select_locale('No METHOD;circular/volume', 'Не задан параметр METHOD: (circular или volume)'))
            return

    except Exception as exc:
        # TODO: log here
        print(exc.with_traceback())


if __name__ == "__main__":
    # main()
    main(user_id='231092888', task_id='1642612066994')
