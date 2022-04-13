import numpy as np


def create_scanline(extendX, extendY, theta_scanline):
    scanline = {}
    scanline['xc'] = extendX[0] + 0.5 * np.diff(extendX)  # mid x
    scanline['yc'] = extendY[0] + 0.5 * np.diff(extendY)  # mid y

    pass
