import os

import numpy as np
import matplotlib.pyplot as plt

from analysis.wavelet.computeWavelet import computeWavelet
from analysis.wavelet.createScanlines import createScanlines
from utils.read_joints import read_joints
import utils.lang as lang
import utils.template as template
from utils.write_json import write_json


def wavelet():

    plt.close()

    print(lang.select_locale('Analyse spacing with wavelet transform','Анализ - Метод вейвлет преобразований'))
    template.wavelet_brief[lang.select_locale('Method', 'Модуль')] = lang.select_locale('Analyse spacing with wavelet transform','Анализ - Метод вейвлет преобразований')


    if 'SCANS' in template.config.keys() and 'DX' in template.config.keys() and 'DY' in template.config.keys():
        nb_scans = template.config['SCANS']
        deltaX = template.config['DX']
        deltaY = template.config['DY']

        if 'THETA' in template.config.keys():
            if 90 >= template.config['THETA'] >= -90:
                THETA = 90 - template.config['THETA']
            else:
                print(
                    lang.select_locale('Theta orientation for scanline should be (-90,90). Will estimate best scanline',
                                       'Значение угла наклона theta для сканирующей линии должно быть в диапазоне (-90,90). Будет выбрана произвольная сканирующая линия.')
                )
                THETA = -999

        else:
            print(
                lang.select_locale('No theta orientation for scanline given by user. Will estimate best scanline',
                                   'Не указано значение угла наклона. Будет выбрана произвольная сканирующая линия.')
            )
            THETA = -999

    else:
        print(lang.select_locale('Missing arguments : SCANS - DX - DY - THETA', 'Не указаны парметры : SCANS - DX - DY - THETA'))
        return

    nodes = read_joints()
    # Scanline PROCESSING
    scanline_info = {}
    scanline_info['nb_scans'] = 30
    scanline_info['nb_lines'] = nb_scans
    scanline_info['dX'] = deltaX
    scanline_info['dY'] = deltaY
    scanline_info['theta'] = np.deg2rad(THETA)
    scanlines = createScanlines(nodes, scanline_info)

    # Wavelet analyse
    computeWavelet(scanlines)

    write_json(template.wavelet_brief, template.config['WAVELET_OUTPUT'])

