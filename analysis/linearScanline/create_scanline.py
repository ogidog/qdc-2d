import numpy as np


def create_scanline(extendX, extendY, theta_scanline):

    scanline = {}
    scanline['xc'] = extendX[0] + 0.5 * np.diff(extendX)  # mid x
    scanline['yc'] = extendY[0] + 0.5 * np.diff(extendY)  # mid y
    scanline['r'] = np.sqrt((0.5 * np.diff((extendX))) ** 2 + (0.5 * np.diff((extendY))) ** 2)  # scanlin length
    scanline['theta_scanline'] = theta_scanline  # scanline angle

    xc = scanline['xc']
    yc = scanline['yc']
    r = scanline['r']

    scanline['Xsl'] = [xc + r * np.cos(theta_scanline),
                       xc + r * np.cos(theta_scanline + np.pi)]  # scanline extremities x
    scanline['Ysl'] = [yc + r * np.sin(theta_scanline),
                       yc + r * np.sin(theta_scanline + np.pi)]  # scanline extremities y
    scanline['Xb']  = [scanline['Xsl'][0][0], scanline['Xsl'][1][0], scanline['Xsl'][1][0],  scanline['Xsl'][0][0], scanline['Xsl'][0][0]] # Rectangle around scanline x coor
    scanline['Yb']  = [scanline['Ysl'][0][0], scanline['Ysl'][0][0], scanline['Ysl'][1][0], scanline['Ysl'][1][0], scanline['Ysl'][0][0]] # Rectangle around scanline y coor

    return scanline
