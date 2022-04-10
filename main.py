import sys
import numpy as np

from TEMPLATES.run_function.run_hough import run_hough
from TEMPLATES.run_function.run_linear import run_linear

template = {}


def read_template_file(file):
    template['jNAME'] = []
    template['jORIENTATION'] = []
    template['jSPACING'] = []

    def switch(line):
        if line[0] == 'SYNTHETIC':
            template["SYNTHETIC"] = float(str.strip(line[1]))
            return
        elif line[0] == 'STEP':
            template['STEP'] = str.strip(line[1])
            return
        elif line[0] == 'METHOD':
            template['METHOD'] = str.strip(line[1])
            return
        elif line[0] == 'INPUT':
            template['INPUT'] = str.strip(line[1])
            return
        elif line[0] == 'OUTPUT':
            template['OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'SCALE':
            template['SCALE'] = np.round(np.float32(str.strip(line[1])))
            return
        elif line[0] == 'NORTH':
            template['NORTH'] = np.array(str.strip(line[1]).split(" "), dtype=np.float32)
            return
        elif line[0] == 'TABLE':
            template['TABLE'] = str.strip(line[1])
            return
        elif line[0] == 'COVER':
            template['COVER'] = np.float64(str.strip(line[1]))
            return
        elif line[0] == 'NB_LINEARSCANS':
            template['NB_LINEARSCANS'] = np.round(np.float64(str.strip(line[1])))
            return
        elif line[0] == 'DX':
            template['DX'] = np.float64(str.strip(line[1]))
            return
        elif line[0] == 'DY':
            template['DY'] = np.float64(str.strip(line[1]))
            return
        elif line[0] == 'SCANS':
            template['SCANS'] = np.round(np.float64(str.strip(line[1])))
            return
        elif line[0] == 'THETA':
            template['THETA'] = np.round(np.float64(str.strip(line[1])))
            return
        elif line[0] == 'CIRCLES':
            template['CIRCLES'] = int(str.strip(line[1]))
            return
        elif line[0] == 'JOINT':
            if len(line) < 4:
                print('Missing information. Needed : JOINT;name;orientation;spacing')
                return

            template['jNAME'].append(str.strip(line[1]))
            template['jORIENTATION'].append(np.float64(str.strip(line[2])))
            template['jSPACING'].append(np.float64(str.strip(line[3])))
            return
        else:
            print('{}: Not used\n'.format(line[0]))

    f = open(file)

    while True:
        line = f.readline()
        if line == "":
            f.close()
            break
        switch(line.split(";"))


def main(template_file="TEMPLATE.txt"):
    try:

        read_template_file(template_file)

        if template['STEP'] == 'HELP' or template['STEP'] == '-h':
            f = open('help.txt', mode="r")
            while True:
                line = f.readline()
                if line == "":
                    f.close()
                    break;
                print(line)

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
                    # run_persistence(template)
                elif template['METHOD'] == "wavelet":
                    print('Analyse spacing with wavelet transform')
                    # run_wavelet(template)
                elif template['METHOD'] == "circular":
                    print('Analyse with circular scanline')
                    # run_circular(template)
                elif template['METHOD'] == "parallelLinear":
                    print()
                    # run_parallelLinear(template)
            else:
                print(
                    'Available method for STEP 3 : hough or linear or parallelLinear or circular or wavelet or persistence')
                return
        else:
            print('No METHOD;hough/linear/persistence')
            return

    except ValueError:
        print(ValueError)


if __name__ == "__main__":
    [template_file] = sys.argv[1:]

    main(template_file)
