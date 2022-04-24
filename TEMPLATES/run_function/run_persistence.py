from analysis.persistance.computePersistence import computePersistence
from read_write_joints.readJoints import readJoints
import matplotlib.pyplot as plt


def run_persistence(template):
    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
        if 'COVER' in template.keys():
            cover  = template['COVER']
            if cover>1 or cover<0:
                print('Cover parameters must be [0:1]')
                return
            elif cover==0:
                nodes = readJoints(joint_file)
                #nodes.synthetic = template.SYNTHETIC;
                #Persistence on overall area
                #figure(1)
                #fprintf('I-- Persistence over the entire window\n')
                #persistance = computePersistance(nodes);
                #fprintf('\n\n')
                #Persistence map
                #figure(2)
                #fprintf('II-- Persistence MAP\n')
                #prompt = 'How many squares to run persistence MAP ?';
                #squares = input(prompt);
                #computePersistanceMap(nodes, squares);
            else:
                nodes = readJoints(joint_file);
                nodes['synthetic'] = template['SYNTHETIC']

                # Persistence on overall area
                plt.figure(1)
                plt.title('I-- Persistence over the entire window')
                print('I-- Persistence over the entire window')
                persistance = computePersistence(nodes, cover)
                plt.show()
                print('')

                # Persistence map
                plt.figure(2)