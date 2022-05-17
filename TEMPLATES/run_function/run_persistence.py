from analysis.persistence.computePersistenceMap import computePersistanceMap
from analysis.persistence.computePersistence import computePersistence
from read_write_joints.readJoints import readJoints
import matplotlib.pyplot as plt


def run_persistence(template):
    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
        if 'COVER' in template.keys():
            cover = float(template['COVER'])
            if cover > 1 or cover < 0:
                print('Cover parameters must be [0:1]')
                return
            elif cover == 0:
                nodes = readJoints(joint_file)
                nodes['synthetic'] = template['SYNTHETIC']
                # Persistence on overall area
                plt.figure(1)
                print('I-- Persistence over the entire window')
                persistance = computePersistence(nodes)
                print('')
                # Persistence map
                plt.figure(2)
                print('II-- Persistence MAP')
                if "SQUARES" in template.keys():
                    squares = int(template['SQUARES'])
                else:
                    prompt = 'How many squares to run persistence MAP ?'
                    squares = int(input(prompt))
                computePersistanceMap(nodes, squares)
            else:
                nodes = readJoints(joint_file)
                nodes['synthetic'] = template['SYNTHETIC']

                # Persistence on overall area
                plt.figure(1)
                plt.title('I-- Persistence over the entire window')
                print('I-- Persistence over the entire window')
                persistance = computePersistence(nodes, cover)
                print('')

                # Persistence map
                plt.figure(2)
                plt.title('II-- Persistence MAP')
                print('II-- Persistence MAP')
                if "SQUARES" in template.keys():
                    squares = int(template['SQUARES'])
                else:
                    prompt = 'How many squares to run persistence ?: ';
                    squares = int(input(prompt))
                computePersistanceMap(nodes, int(squares))
                plt.show()

                print('')

        else:  # no cover given
            nodes = readJoints(joint_file)
            if "SQUARES" in template.keys():
                squares = int(template['SQUARES'])
            else:
                prompt = 'How many squares to run persistence ?'
                squares = int(input(prompt))
            plt.figure(1)
            computePersistanceMap(nodes, squares)

        return persistance

    else:
        print('Missing arguments : INPUT(mandatory) - COVER(optional)')
        return
