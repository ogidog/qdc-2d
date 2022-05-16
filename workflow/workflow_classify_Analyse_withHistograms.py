import os

from matplotlib import pyplot as plt

from classify._withHistograms.classify_fromGaussians import classify_fromGaussians
from classify._withHistograms.find_jointSetLimits import find_jointSetLimits
from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram
from read_write_joints.readJoints import readJoints


def workflow_classify_Analyse_withHistograms(nodes, outPath):
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
        nodes = readJoints(joint_file)
        pass

    # return summarizeTable, files
