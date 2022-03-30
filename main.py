import sys
import numpy as np

template = {}


def read_template_file(file):
    def switch(line):
        if line[0] == 'SYNTHETIC':
            template["SYNTHETIC"] = float(str.strip(line[1]))
            return
        if line[0] == 'STEP':
            template['STEP'] = int(str.strip(line[1]))
            return
        if line[0] == 'METHOD':
            template['METHOD'] = str.strip(line[1])
            return
        if line[0] == 'INPUT':
            template['INPUT'] = str.strip(line[1])
            return
        if line[0] == 'OUTPUT':
            template['OUTPUT'] = str.strip(line[1])
            return
        if line[0] == 'SCALE':
            template['SCALE'] = np.round(np.float32(str.strip(line[1])))
            return
        if line[0] == 'NORTH':
            template['NORTH'] = np.array(str.strip(line[1]).split(" "), dtype=np.float32)
            return
        if line[0] == 'TABLE':
            template['TABLE'] = str.strip(line[1])
            return
        if line[0] == 'COVER':
            template['COVER'] = np.float64(str.strip(line[1]))
            return
        if line[0] == 'NB_LINEARSCANS':
            template['NB_LINEARSCANS'] = np.round(np.float64(str.strip(line[1])))
            return
        if line[0] == 'DX':
            template['DX'] = np.float64(str.strip(line[1]))
            return
        if line[0] == 'DY':
            template['DY'] = np.float64(str.strip(line[1]))
            return
        if line[0] == 'SCANS':
            template['SCANS'] = np.round(np.float64(str.strip(line[1])))
            return
        if line[0] == 'THETA':
            template['THETA'] = np.round(np.float64(str.strip(line[1])))
            return
        if line[0] == 'JOINT':
            if len(line) < 4:
                print('Missing information. Needed : JOINT;name;orientation;spacing')
                return

            joint = len(template['jNAME'])
            template['jNAME'] = []
            template['jNAME'][joint] = str.strip(line[1])

            template['jORIENTATION'] = []
            template['jORIENTATION'][joint] = np.float64(str.strip(line[2]))

            template['jSPACING'] = []
            template['jSPACING'][joint] = np.float64(str.strip(line[3]))
            return

        print('{} : Not used\n'.format(str.strip(line[1])))

    f = open(template_file)

    while True:
        line = f.readline()

        if line == "":
            f.close()
            break

        switch(line.split(";"))


def main(template_file="TEMPLATE.txt"):
    read_template_file(template_file)
    print()


if __name__ == "__main__":
    [template_file] = sys.argv[1:]

    main(template_file)
