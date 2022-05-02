import numpy as np


def computeWavelet(scanline):
    for scan in range(len(scanline['iD'])):
        X_trans = scanline['X_trans'][scan]
        dist = np.sqrt((scanline['maxX'][scan] - scanline['minX'][scan]) ** 2 + (
                scanline['maxY'][scan] - scanline['minY'][scan]) ** 2)
        s = np.append(np.arange(0, dist, dist / 100), dist)

        index = np.zeros((len(X_trans), 1))
        index[:] = np.NaN
        for i in range(len(X_trans)):
            d = dist
            for j in range(len(s)):
                if abs(X_trans(i) - s(j)) < d
                    d = abs(X_trans(i) - s(j));
                    index(i) = j

        pass
