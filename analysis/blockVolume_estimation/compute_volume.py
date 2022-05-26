import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

import utils.lang as lang
import utils.template as template
from utils.write_plot import write_plot


def compute_volume(w):
    NBjoints = np.size(w, 0)
    if NBjoints == 1:
        print(lang.select_locale('1 jointset', '1 набор линий'))
        Vb = 50 * w[0, 1] ** 3
    elif NBjoints == 2:
        print(lang.select_locale('2 jointset', '2 набора линий'))
        Vb = 5 * w[0, 1] ** 2 * w[1, 1]
    elif NBjoints == 3:
        print(lang.select_locale('3 jointset', '3 набора линий'))
        ori = np.sort(w[:, 0])
        g1 = np.abs(ori[0] - ori[1])
        g2 = np.abs(ori[1] - ori[2])
        g3 = np.abs(ori[2] - ori[0])
        Vb = w[0, 1] * w[1, 1] * w[2, 1] / (np.sin(np.deg2rad(g1)) * np.sin(np.deg2rad(g2)) * np.sin(np.deg2rad(g3)))
    else:
        print(lang.select_locale('You should not consider more than 3 jointsets',
                                 'Более 3 наборов линий не поддерживается'))
        Vb = -1

    if Vb != -1:
        print(lang.select_locale('Vb value : {}', 'Vb : {}').format(Vb))
        wfc.volume_brief[lang.select_locale('Vb value', 'Vb')] = Vb

    spacing = np.sort(w[:, 1])
    if len(spacing) == 3:
        a3 = spacing[2] / spacing[0]
        a2 = spacing[1] / spacing[0]
    elif len(spacing) == 2:
        print(lang.select_locale('\n!!!!WARNING : Plotting blockshape for only 2 joints can be wrong !!!!',
                                 '!!!!Внимание : Отрисовка формы блока для 2 наборов линий может быть некорректна !!!!'))
        a3 = spacing[1] / spacing[0]
        a2 = spacing[1] / spacing[0]
    else:
        print(lang.select_locale('\n!!!!WARNING : Plotting blockshape for only 2 joints can be wrong !!!!',
                                 '!!!!Внимание : Отрисовка формы блока для 1 наборов линий может быть некорректна !!!!'))
        a3 = spacing[0] / spacing[0]
        a2 = spacing[0] / spacing[0]

    B = [a2, a3]
    # Block shape factor
    Beta = (a2 + a2 * a3 + a3) ** 3 / (a2 * a3) ** 2

    print(lang.select_locale('Alpha2: {} -- Alpha3: {}', 'Alpha2: {} -- Alpha3: {}').format(*B))
    wfc.volume_brief[lang.select_locale('Alpha2 -- Alpha3', 'Alpha2 -- Alpha3')] = [*B]

    print(lang.select_locale('Block shape factor : {}', 'Коэффициент формы блока : {}').format(Beta))
    wfc.volume_brief[lang.select_locale('Block shape factor', 'Коэффициент формы блока')] = Beta

    # Do the actual plotting
    img_file = os.path.dirname(__file__) + os.path.sep + "img_blockShape.PNG"
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
    ax1.set_xlabel('$\\alpha_3$ = ' + lang.select_locale('largest spacing / smallest spacing',
                                                         'наибольший интервал / наименьший интервал'))
    ax1.set_ylabel('$\\alpha_2$ = ' + lang.select_locale('medium spacing / smallest spacing',
                                                         'средний интервал / наименьший интервал'))
    txt = '$\\leftarrow$ ' + lang.select_locale('Block type', 'Тип блока')
    ax1.text(a3, a2, txt, verticalalignment="center_baseline")

    ax2 = fig.add_subplot(1, 1, 1, label="ax2")
    ax2.imshow(im, aspect="auto")
    ax2.set_zorder(1)
    ax2.set_xticks([])
    ax2.set_yticks([])

    plt.title(lang.select_locale('Block types analysis with the block shape factor',
                                 'Анализ типов блока с учетом коэффициента формы'))
    # plt.savefig(
    #     template.config["VOLUME_OUTPUT"] + os.path.sep + "fig1_" + str(wfc.classif_joint_set_counter) + ".png",
    #     dpi=300)

    write_plot(plt)
    plt.show()

    return Vb
