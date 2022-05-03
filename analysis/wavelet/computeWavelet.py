import numpy as np
from ghostipy.spectral import cwt, MorseWavelet
from matplotlib import pyplot as plt


def computeWavelet(scanline):
    for scan in range(len(scanline['iD'])):
        X_trans = scanline['X_trans'][scan]
        dist = np.sqrt((scanline['maxX'][scan] - scanline['minX'][scan]) ** 2 + (
                scanline['maxY'][scan] - scanline['minY'][scan]) ** 2)
        s = np.append(np.arange(0, dist, dist / 100), dist)

        index = np.zeros(len(X_trans))
        for i in range(len(X_trans)):
            d = dist
            for j in range(len(s)):
                if np.abs(X_trans[i] - s[j]) < d:
                    d = np.abs(X_trans[i] - s[j])
                    index[i] = j
        index = np.array(index, dtype=int)

        wave = np.zeros(len(s))
        wave[index] = 10

        # -- Plot wavelet analysis
        plt.figure(scan + 2)
        plt.subplots(constrained_layout=True)
        plt.subplot(211)
        plt.axhline(y=1, color='k', linestyle='-', label='Scanline')
        plt.xlim([0, len(wave)])
        plt.ylim([0.5, 1.5]);
        plt.plot(index, np.ones(len(index)), 'rx')
        plt.text(len(wave) / 2, 1.08, 'Scanline', rotation=360)

        # -- Wavelet analysis
        plt.subplot(212)
        mtlb = wave
        Fs = 1
        tms = np.array(np.arange(0, len(mtlb)) / Fs, dtype=np.int)
        [cfs, _, frq, *rest] = cwt(mtlb, fs=1, wavelet=MorseWavelet(gamma=3, beta=60))
        plt.pcolor(tms, frq, np.abs(cfs))
        plt.xlabel('Position on scanline')
        plt.ylabel('Scale')
        if scanline['iD'][scan] == 0:  # Main scanline
            plt.title('Main scanline')
        else:
            title_string = 'dX: {} - dY: {}'.format(scanline['dX'][scan], scanline['dY'][scan])
            plt.title(title_string)

        plt.show()
