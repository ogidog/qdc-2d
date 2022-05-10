from matplotlib import pyplot as plt

from classify._withHistograms.find_jointSet_fromHistogram import find_jointSet_fromHistogram


def workflow_classify_Analyse_withHistograms(nodes, outPath):

    plt.close()

    # -- Classification
    gaussianParams = find_jointSet_fromHistogram(nodes)
    #limits = find_jointSetLimits(gaussianParams);
    #classify_fromGaussians(limits, nodes, outPath);

    # return summarizeTable, files