import matplotlib.pyplot as plt

from read_write_joints.readJoints import readJoints


def main(inputFile='D:\Temp\-QDC-2D-main\TEMPLATES\examples\createdJoints1.txt',
         outputFolder='D:\Temp\-QDC-2D-main\TEMPLATES\examples\classif.txt'):

    plt.close()

    nodes = readJoints(inputFile)
    summarizeTable = workflow_classify_Analyse_withHistograms(nodes, outputFolder)


if __name__ == "__main__":
    main()
