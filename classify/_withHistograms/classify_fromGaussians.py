import os
import numpy as np

from utils.splitNodes_per_setID import splitNodes_per_setID
from utils.writeJoints import writeJoints
import utils.template as template
import utils.lang as lang

def classify_fromGaussians(limits):
    if limits == -1:
        print(lang.select_locale('Only 1 jointset selected -- No need for classification', 'Выбран один набор линий - Классификация не требуется'))
        nodes_classif = template.nodes
        return nodes_classif

    # Classify jointSet
    print(lang.select_locale('Classification of joint set --> Started', 'Классификация набора линий --> Старт'))
    template.nodes['setiD'] = []
    for i in range(len(template.nodes['iD'])):
        joint_orientation = template.nodes['ori_mean_deg'][i]
        for inter in range(len(limits) - 1):
            if joint_orientation >= limits[inter] and joint_orientation < limits[inter + 1]:
                template.nodes['setiD'].append(inter + 1)

        if joint_orientation >= limits[-1] or joint_orientation < limits[0]:
            template.nodes['setiD'].append(0)

    nodes_classif = template.nodes

    # Split nodes and write in OutPath
    output_file_template = template.config['OUTPUT'] + os.path.sep + "classif.txt"
    for set in range(len(limits)):
        out = output_file_template.replace('.', ('_{}classif.'.format(str(set))))
        split_nodes = splitNodes_per_setID(nodes_classif, set)
        split_matrice = writeJoints(split_nodes)
        np.savetxt(out, split_matrice, fmt="%d,%.10f,%.10f;", delimiter=",")

    print(lang.select_locale('Classification of joint set --> DONE!', 'Классификация набора линий --> Завершено'));

    return nodes_classif
