import os

import matplotlib.pyplot as plt

from analysis.persistence.computePersistenceMap import computePersistanceMap
from analysis.persistence.computePersistence import computePersistence
from utils.read_joints import read_joints
from utils.write_json import write_json
import utils.template as template

import utils.lang as lang


def persistence():

    plt.close()

    print(lang.select_locale('Analyse the persistence','Анализ - Постоянство линий'))
    template.persistence_brief[lang.select_locale('Method', 'Модуль')] = lang.select_locale('Analyse the persistence','Анализ - Постоянство линий')

    if 'COVER' in template.config.keys():
        cover = float(template.config['COVER'])
        if cover > 1 or cover < 0:
            print(lang.select_locale("Covering parameters should be [0, 1]",
                                     'Коэффициент покрытия должны быть в интервале [0, 1]'))
            return None

        elif cover == 0:
            nodes = read_joints()
            nodes['synthetic'] = template.config['SYNTHETIC']

            # Persistence on overall area
            print(lang.select_locale('I -- Persistence over the entire window\n',
                                     'I -- Расчет постоянства по всему окну\n'))
            persistance = computePersistence(nodes)

            print('')

            # Persistence map
            print(lang.select_locale('II-- Persistence MAP\n', '\nII-- Карта постоянства\n'))
            if "SQUARES" in template.config.keys():
                squares = int(template.config['SQUARES'])
            else:
                prompt = lang.select_locale("How many squares to run persistence MAP?",
                                            'Количество квадратных областей для расчета карты постоянства?')
                squares = int(input(prompt))

            computePersistanceMap(nodes, squares)

        else:
            nodes = read_joints()
            nodes['synthetic'] = template.config['SYNTHETIC']

            # Persistence on overall area
            print(lang.select_locale('I -- Persistence over the entire window\n',
                                     'I -- Расчет постоянства по всему окну\n'))
            persistance = computePersistence(nodes, cover)

            print('')

            # Persistence map
            print(lang.select_locale('II-- Persistence MAP\n', '\nII-- Карта постоянства\n'))
            if "SQUARES" in template.config.keys():
                squares = int(template.config['SQUARES'])
            else:
                prompt = lang.select_locale("How many squares to run persistence MAP?",
                                            'Количество квадратных областей для расчета карты постоянства?')
                squares = int(input(prompt))

            computePersistanceMap(nodes, int(squares))

    else:  # no cover given
        nodes = read_joints()
        if "SQUARES" in template.config.keys():
            squares = int(template.config['SQUARES'])
        else:
            prompt = lang.select_locale("How many squares to run persistence MAP?",
                                        'Количество квадратных областей для расчета карты постоянства?')
            squares = int(input(prompt))

        computePersistanceMap(nodes, squares)

    write_json(template.persistence_brief, template.config['PERSISTENCE_OUTPUT'])

    return persistance
