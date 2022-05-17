import os

from matplotlib import pyplot as plt

from TEMPLATES.run_function.run_circular import run_circular
from TEMPLATES.run_function.run_hough import run_hough
from TEMPLATES.run_function.run_linear import run_linear
from TEMPLATES.run_function.run_persistence import run_persistence
from classify._withHistograms.classify_fromGaussians import classify_fromGaussians
from classify._withHistograms.find_jointSetLimits import find_jointSetLimits
from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram
from read_write_joints.readJoints import readJoints
from read_write_joints.read_template_file import read_template_file


def workflow_classify_Analyse_withHistograms(nodes, outPath, templatefile):
    plt.close()

    # -- Classification
    gaussianParams = find_jointSet_fromHistogram(nodes)
    limits = find_jointSetLimits(gaussianParams)
    classify_fromGaussians(limits, nodes, outPath)

    fullpath = os.path.dirname(outPath)
    files = list(filter(lambda file: "classif" in file, os.listdir(fullpath)))

    print('---------STARTING ANALYSIS---------')
    for j in range(len(files)):
        joint_file = fullpath + os.path.sep + files[j]
        print('--- File : {}'.format(joint_file))
        set_iD = int(files[j].split('_')[-1].split("classif")[0])

        template = read_template_file(templatefile)
        template['INPUT'] = joint_file

        # hough analyse
        # nodes = run_hough(template)

        # linear analyse
        # [frequency, spacing_real] = run_linear(template)

        # circular scanline
        #[intensity_estimator, density_estimator, traceLength_estimator] = run_circular(template)

        # persistance
        # persistance = run_persistence(template)

        pass

    # return summarizeTable, files
