import numpy as np
import matplotlib.pyplot as plt

from analysis.wavelet.computeWavelet import computeWavelet
from analysis.wavelet.createScanlines import createScanlines
from utils.read_joints import read_joints


def wavelet(template):
    plt.close()
    if 'INPUT' in template.keys() and 'SCANS' in template.keys() and 'DX' in template.keys() and 'DY' in template.keys():
        joint_path = template['INPUT']
        nb_scans = template['SCANS']
        deltaX = template['DX']
        deltaY = template['DY']

        if 'THETA' in template.keys():
            if 90 >= template['THETA'] >= -90:
                THETA = 90 - template['THETA']
            else:
                print('Theta orientation for scanline should be (-90,90). Will estimate best scanline')
                THETA = -999

        else:
            print('No theta orientation for scanline given by user. Will estimate best scanline')
            THETA = -999

    else:
        print('Missing arguments : INPUT - SCANS - DX - DY - THETA')
        return

    nodes = read_joints(joint_path)
    # Scanline PROCESSING
    scanline_info = {}
    scanline_info['nb_scans'] = 30
    scanline_info['nb_lines'] = nb_scans
    scanline_info['dX'] = deltaX
    scanline_info['dY'] = deltaY
    scanline_info['theta'] = np.deg2rad(THETA)
    plt.figure(1)
    scanlines = createScanlines(nodes, scanline_info)
    plt.show()

    # Wavelet analyse
    computeWavelet(scanlines)

