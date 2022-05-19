import os

from matplotlib import pyplot as plt

from TEMPLATES.run_function.run_circular import run_circular
from TEMPLATES.run_function.run_hough import run_hough
from TEMPLATES.run_function.run_linear import run_linear
from TEMPLATES.run_function.run_persistence import run_persistence
from TEMPLATES.run_function.run_volume import run_volume
from TEMPLATES.run_function.run_wavelet import run_wavelet
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

    resume = {'SetId':[], "nbTraces":[], 'orientation_mean':[],
              'orientation_min':[], 'orientation_max':[], 'length_mean':[],
              'length_min':[], 'length_max':[], 'spacing_mean_linearScanline':[],
              'spacing_min_linearScanline':[], 'spacing_max_linearScanline':[],
              'spacing_mean_houghAnalyse':[], 'spacing_min_houghAnalyse':[],
              'spacing_max_houghAnalyse':[], 'persistence_mean':[], 'persistence_min':[],
              'persistence_max':[], 'spacing_frequency':[], 'intensity_estimator':[],
              'density_estimator':[],'traceLength_estimator':[]}

    print('---------STARTING ANALYSIS---------')
    for j in range(len(files)):
        joint_file = fullpath + os.path.sep + files[j]
        print('--- File : {}'.format(joint_file))
        set_iD = int(files[j].split('_')[-1].split("classif")[0])

        template = read_template_file(templatefile)
        template['INPUT'] = joint_file

        # hough analyse
        nodes = run_hough(template)

        # linear analyse
        # [frequency, spacing_real] = run_linear(template)

        # circular scanline
        #[intensity_estimator, density_estimator, traceLength_estimator] = run_circular(template)

        # persistance
        # persistance = run_persistence(template)

        # volume
        # run_volume(template)

        # wavelet
        # run_wavelet(template)

        # -- summarize
        resume.SetId{j,1}                   = set_iD{1};
        resume.nbTraces{j,1}                = length(nodes.iD);
        orientations = mean_orientation(nodes);
        resume.orientation_mean{j,1}        = orientations.MEAN;
        resume.orientation_min{j,1}         = orientations.MIN;
        resume.orientation_max{j,1}         = orientations.MAX;
        resume.length_mean{j,1}             = mean(cell2mat(nodes.norm));
        resume.length_min{j,1}              = min(cell2mat(nodes.norm));
        resume.length_max{j,1}              = max(cell2mat(nodes.norm));
        resume.spacing_mean_linearScanline{j,1} = mean(spacing_real);
        resume.spacing_min_linearScanline{j,1}  = min(spacing_real);
        resume.spacing_max_linearScanline{j,1}  = max(spacing_real);
        resume.spacing_mean_houghAnalyse{j,1}   = mean(nodes.real_spacing_hough);
        resume.spacing_min_houghAnalyse{j,1}    = min(nodes.real_spacing_hough);
        resume.spacing_max_houghAnalyse{j,1}    = max(nodes.real_spacing_hough);
        resume.persistence_mean{j,1}        = mean(persistance);
        resume.persistence_min{j,1}         = min(persistance);
        resume.persistence_max{j,1}         = max(persistance);
        resume.spacing_frequency{j,1}       = frequency;
        resume.intensity_estimator{j,1}     = intensity_estimator;
        resume.density_estimator{j,1}       = density_estimator;
        resume.traceLength_estimator{j,1}   = traceLength_estimator;

        pass

    # return summarizeTable, files
