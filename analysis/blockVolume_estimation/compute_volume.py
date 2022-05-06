import numpy as np


def compute_volume(w):
    NBjoints = np.size(w, 0)
    if NBjoints == 1:
        print('1 jointset')
        Vb = 50 * w[0, 1] ** 3
    elif NBjoints == 2:
        print('2 jointsets')
        Vb = 5 * w[0, 1] ** 2 * w[1, 1]
    elif NBjoints == 3:
        print('3 jointsets')
        ori = np.sort(w[:, 0])
        g1 = np.abs(ori[0] - ori[1])
        g2 = np.abs(ori[1] - ori[2])
        g3 = np.abs(ori[2] - ori[0])
        Vb = w[0, 1] * w[1, 1] * w[2, 1] / (np.sin(np.deg2rad(g1)) * np.sin(np.deg2rad(g2)) * np.sin(np.deg2rad(g3)))
    else:
        print('You should not consider more than 3 jointsets')
        Vb = -1

    if Vb != -1:
        print('Vb value : {}'.format(Vb))

    spacing = np.sort(w[:,1])


    return Vb
