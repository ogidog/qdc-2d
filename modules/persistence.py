import os

from analysis.persistence.computePersistenceMap import computePersistanceMap
from analysis.persistence.computePersistence import computePersistence
from utils.readJoints import readJoints
from utils.write_json import write_json
import utils.template as template

import utils.lang as lang


def persistence(template):
    if 'INPUT' in template.keys():
        joint_file = template['INPUT']

        if not os.path.exists(template['PERSISTENCE_OUTPUT']):
            os.makedirs(template['PERSISTENCE_OUTPUT'])

        if 'COVER' in template.keys():
            cover = float(template['COVER'])
            if cover > 1 or cover < 0:
                print(lang.select_locale("Covering parameters should be [0, 1]",
                                         'Коэффициент покрытия должны быть в интервале [0, 1]'))
                return

            elif cover == 0:
                nodes = readJoints(joint_file)
                nodes['synthetic'] = template['SYNTHETIC']

                # Persistence on overall area
                print(lang.select_locale('I -- Persistence over the entire window\n',
                                         'I -- Расчет постоянства по всему окну\n'))
                persistance = computePersistence(nodes)

                print('')

                # Persistence map
                print(lang.select_locale('II-- Persistence MAP\n', '\nII-- Карта постоянства\n'))
                if "SQUARES" in template.keys():
                    squares = int(template['SQUARES'])
                else:
                    prompt = lang.select_locale("How many squares to run persistence MAP?",
                                                'Количество квадратных областей для расчета карты постоянства?')
                    squares = int(input(prompt))
                computePersistanceMap(nodes, squares)

            else:
                nodes = readJoints(joint_file)
                nodes['synthetic'] = template['SYNTHETIC']

                # Persistence on overall area
                print(lang.select_locale('I -- Persistence over the entire window\n',
                                         'I -- Расчет постоянства по всему окну\n'))
                persistance = computePersistence(nodes, cover)

                print('')

                # Persistence map
                print(lang.select_locale('II-- Persistence MAP\n', '\nII-- Карта постоянства\n'))
                if "SQUARES" in template.keys():
                    squares = int(template['SQUARES'])
                else:
                    prompt = lang.select_locale("How many squares to run persistence MAP?",
                                                'Количество квадратных областей для расчета карты постоянства?')
                    squares = int(input(prompt))

                computePersistanceMap(nodes, int(squares))

        else:  # no cover given
            nodes = readJoints(joint_file)
            if "SQUARES" in template.keys():
                squares = int(template['SQUARES'])
            else:
                prompt = lang.select_locale("How many squares to run persistence MAP?",
                                            'Количество квадратных областей для расчета карты постоянства?')
                squares = int(input(prompt))

            computePersistanceMap(nodes, squares)

        write_json(wfc.persistence_brief,
                   template.config['PERSISTENCE_OUTPUT'] + os.path.sep + "brief_" + str(wfc.classif_joint_set_counter) + ".json")

        return persistance

    else:
        print(lang.select_locale('Missing arguments : INPUT - COVER',
                                 'Не заданы обязательные параметры : ФАЙЛ ЛИНИЙ, КОЭФФИЦИЕНТ ПОКРЫТИЯ'))
