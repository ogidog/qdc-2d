import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


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

    spacing = np.sort(w[:, 1])
    if len(spacing) == 3:
        a3 = spacing[2] / spacing[0]
        a2 = spacing[1] / spacing[0]
    elif len(spacing) == 2:
        print('!!!!WARNING : Plotting blockshape for only 2 joints can be wrong !!!!')
        a3 = spacing[1] / spacing[0]
        a2 = spacing[1] / spacing[0]
    else:  # length(spacing) == 1
        print('!!!!WARNING : Plotting blockshape for only 1 joint is wrong !!!!')
        a3 = spacing[0] / spacing[0]
        a2 = spacing[0] / spacing[0]

    B = [a2, a3]
    # Block shape factor
    Beta = (a2 + a2 * a3 + a3) ** 3 / (a2 * a3) ** 2
    print('Alpha2: {} -- Alpha3: {}'.format(*B))
    print('Block shape factor : {}'.format(Beta))

    # Do the actual plotting
    # im = plt.imread(
    #    os.getcwd() + os.path.sep + "analysis" + os.path.sep + "blockVolume_estimation" + os.path.sep + "img_blockShape.PNG")
    img_file = os.getcwd() + os.path.sep + "analysis" + os.path.sep + "blockVolume_estimation" + os.path.sep + "img_blockShape.PNG"
    im = Image.open(img_file)
    im_size = im.size
    im_data = np.array(im.getdata(0)).reshape(im_size)

    fig = plt.figure(1)
    ax1 = fig.add_subplot(1, 1, 1, facecolor='None', label="ax1")
    xrng = [1, 100]
    yrng = [1, 50]
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_ylim(yrng)
    ax1.set_xlim(xrng)
    ax1.loglog(a3, a2, 'ro', markersize=5)
    ax1.set_zorder(10)
    ax1.set_xlabel('$\\alpha_3$ = largest spacing / smallest spacing')
    ax1.set_ylabel('$\\alpha_2$ = medium spacing / smallest spacing')
    txt = ' $\\leftarrow$ Block type'
    ax1.text(a3, a2, txt, verticalalignment="center_baseline")

    ax2 = fig.add_subplot(1, 1, 1, label="ax2")
    ax2.imshow(im, aspect="auto")
    ax2.set_zorder(1)
    ax2.set_xticks([])
    ax2.set_yticks([])

    plt.title('Block types analysis with the block shape factor')
    plt.show()

    return Vb
