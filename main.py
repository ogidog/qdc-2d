import sys

from TEMPLATES.run_function.run_circular import run_circular
from TEMPLATES.run_function.run_hough import run_hough
from TEMPLATES.run_function.run_linear import run_linear
from TEMPLATES.run_function.run_persistence import run_persistence
from TEMPLATES.run_function.run_volume import run_volume
from TEMPLATES.run_function.run_wavelet import run_wavelet
from read_write_joints.read_template_file import read_template_file


def main(template_file="TEMPLATE.txt"):
    try:

        template = read_template_file(template_file)

        if template['STEP'] == 'HELP' or template['STEP'] == '-h':
            f = open('help.txt', mode="r")
            while True:
                line = f.readline()
                if line == "":
                    f.close()
                    break
                print(line)

        # -- Step 2 : Classify joints
        if template['STEP'] == 2:
            print('STEP 2 : Classify joints')
            if 'METHOD' in template.keys():
                if template.METHOD == "hough":
                    print('Classify with Hough')
                    #UI_classif_withHough()
                elif template['METHOD'] == "histo":
                    print('Classify with oriention histograms')
                    #UI_classif_withGauss()
                else:
                    print('Available method for STEP 2 : histo or hough')
                    return
            else:
                print('No METHOD:histo/hough')
                return

        # -- Step 3 : Analysis 1 jointset
        if int(template['STEP']) == 3:
            print('STEP 3 : Analyse jointset')
            if 'METHOD' in template.keys():
                if template['METHOD'] == "hough":
                    print('Analyse with Hough frame')
                    run_hough(template)
                elif template['METHOD'] == "linear":
                    print('Analyse with linear scanline')
                    run_linear(template)
                elif template['METHOD'] == "persistence":
                    print('Analyse the persistence')
                    run_persistence(template)
                elif template['METHOD'] == "wavelet":
                    print('Analyse spacing with wavelet transform')
                    run_wavelet(template)
                elif template['METHOD'] == "circular":
                    print('Analyse with circular scanline')
                    run_circular(template)
                elif template['METHOD'] == "parallelLinear":
                    print()
                    # run_parallelLinear(template)
            else:
                print(
                    'Available method for STEP 3 : hough or linear or parallelLinear or circular or wavelet or persistence')
                return
        else:
            print('No METHOD;hough/linear/persistence')

        # -- Step 4 : Analysis all jointsets
        if int(template['STEP']) == 4:
            print('STEP 4 : Characterization of the jointing degree ')
            if 'METHOD' in template.keys():
                if template['METHOD'] == "circular":
                    print('Analyse circular scanline')
                    run_circular(template)
                elif template['METHOD'] == "volume":
                    print('Analyse block volume and volume joint count')
                    run_volume(template)
            else:
                print('Available method for STEP 4 : circular or volume')
                return
        else:
            print('No METHOD;circular/volume')

    except ValueError:
        print(ValueError)


if __name__ == "__main__":
    [template_file] = sys.argv[1:]

    main(template_file)
