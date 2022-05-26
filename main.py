from modules.circular import circular
from modules.hough import hough
from modules.linear import linear
from modules.persistence import persistence
from modules.volume import volume
from modules.wavelet import wavelet
import utils.template as template
from utils.readJoints import readJoints


def main():
    try:

        if template.config['STEP'] == 'HELP' or template.config['STEP'] == '-h':
            f = open('help.txt', mode="r")
            while True:
                line = f.readline()
                if line == "":
                    f.close()
                    break
                print(line)

        # -- Step 2 : Classify joints
        if template.config['STEP'] == 2:
            print('STEP 2 : Classify joints')
            if 'METHOD' in template.config.keys():
                if template.config.METHOD == "hough":
                    print('Classify with Hough')
                    #UI_classif_withHough()
                elif template.config['METHOD'] == "histo":
                    print('Classify with oriention histograms')
                    #UI_classif_withGauss()
                else:
                    print('Available method for STEP 2 : histo or hough')
                    return
            else:
                print('No METHOD:histo/hough')
                return

        # -- Step 3 : Analysis 1 jointset
        if int(template.config['STEP']) == 3:
            # print('STEP 3 : Analyse jointset')
            print('Шаг 3 : Анализ набора линий\n')
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "hough":
                    # print('Analyse with Hough frame')
                    print('Анализ - Метод Хафа')
                    hough()
                    return
                elif template.config['METHOD'] == "linear":
                    # print('Analyse with linear scanline')
                    print('Анализ - Линейная разверткой\n')
                    linear()
                    return
                elif template.config['METHOD'] == "persistence":
                    print('Analyse the persistence')
                    persistence()
                    return
                elif template.config['METHOD'] == "wavelet":
                    print('Analyse spacing with wavelet transform')
                    wavelet()
                    return
                elif template.config['METHOD'] == "circular":
                    print('Analyse with circular scanline')
                    circular()
                    return
                elif template.config['METHOD'] == "parallelLinear":
                    pass
                    # parallelLinear()
            else:
                print(
                    'Available method for STEP 3 : hough or linear or parallelLinear or circular or wavelet or persistence')
                return
        else:
            print('No METHOD;hough/linear/persistence')

        # -- Step 4 : Analysis all jointsets
        if int(template.config['STEP']) == 4:
            print('STEP 4 : Characterization of the jointing degree ')
            if 'METHOD' in template.config.keys():
                if template.config['METHOD'] == "circular":
                    print('Analyse circular scanline')
                    circular()
                    return
                elif template.config['METHOD'] == "volume":
                    print('Analyse block volume and volume joint count')
                    volume()
                    return
            else:
                print('Available method for STEP 4 : circular or volume')
                return
        else:
            print('No METHOD;circular/volume')

    except ValueError:
        print(ValueError)


if __name__ == "__main__":

    # TODO: For tests only
    #
    var_config_json = '{"jNAME":["j1","j2","j3"],"jORIENTATION":[10.0,40.0,100.0],"jSPACING":[5.0,10.0,10.0],"G_MEAN":[5.0,1.0],"G_STD":[7.0,9.0],"G_N":[69.0,22.0],"SYNTHETIC":0,"STEP":"3","METHOD":"hough","THETA":10.0,"SCALE":10.0,"COVER":0.9,"CIRCLES":5,"SQUARES":5,"SCANS":2.0,"G_NOISE":2,"DX":2.0,"DY":2.0}'
    nodes = readJoints("examples/example/createdJoints1.txt")
    ######################

    template.config = template.init(var_config_json)
    template.nodes = nodes

    main()
