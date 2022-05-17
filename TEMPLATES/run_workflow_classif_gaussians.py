import matplotlib.pyplot as plt

from read_write_joints.readJoints import readJoints
from workflow.workflow_classify_Analyse_withHistograms import workflow_classify_Analyse_withHistograms


def main(inputFile='D:\intellij-idea-workspace\qdc-2d\TEMPLATES\examples\createdJoints1.txt',
         outputFolder='D:\intellij-idea-workspace\qdc-2d\TEMPLATES\examples\classif.txt',
         templatefile='D:\intellij-idea-workspace\qdc-2d\TEMPLATE.txt'):

    plt.close()

    nodes = readJoints(inputFile)
    summarizeTable = workflow_classify_Analyse_withHistograms(nodes, outputFolder, templatefile)


if __name__ == "__main__":
    main()
