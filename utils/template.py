import json
import os
import numpy as np
from dotenv import dotenv_values

hough_brief = {}
linear_brief = {}
optimization_brief = {}
circular_brief = {}
persistence_brief = {}
volume_brief = {}
config = {}
nodes = []
classif_joint_set_counter = 0


def read_from_txt_file(file):
    template = {}
    template['jNAME'] = []
    template['jORIENTATION'] = []
    template['jSPACING'] = []
    template['G_MEAN'] = []
    template['G_STD'] = []
    template['G_N'] = []

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
        elif line[0] == 'LANG':
            template['LANG'] = str.strip(line[1])
            return
        elif line[0] == 'INPUT':
            template['INPUT'] = str.strip(line[1])
            return
        elif line[0] == 'OUTPUT':
            template['OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'SCALE':
            template['SCALE'] = np.round(np.float64(str.strip(line[1])))
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
        elif line[0] == 'SQUARES':
            template['SQUARES'] = int(str.strip(line[1]))
            return
        elif line[0] == 'GAUSS_NOISE':
            template['G_NOISE'] = int(str.strip(line[1]))
            return
        elif line[0] == 'OUTPUT':
            template['OUTPUT_PATH'] = str.strip(line[1])
            return
        elif line[0] == 'OUTPUT_TYPE':
            template['OUTPUT_TYPE'] = str.strip(line[1])
            return
        elif line[0] == 'LINEAR_OUTPUT':
            template['LINEAR_OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'HOUGH_OUTPUT':
            template['HOUGH_OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'CIRCULAR_OUTPUT':
            template['CIRCULAR_OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'OPTIMIZATION_OUTPUT':
            template['OPTIMIZATION_OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'PERSISTENCE_OUTPUT':
            template['PERSISTENCE_OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'VOLUME_OUTPUT':
            template['VOLUME_OUTPUT'] = str.strip(line[1])
            return
        elif line[0] == 'JOINT':
            if len(line) < 4:
                print('Missing information. Needed : JOINT;name;orientation;spacing')
                return

            template['jNAME'].append(str.strip(line[1]))
            template['jORIENTATION'].append(np.float64(str.strip(line[2])))
            template['jSPACING'].append(np.float64(str.strip(line[3])))
            return
        elif line[0] == 'GAUSS':
            if len(line) < 4:
                print('Missing information. Needed : JOINT;mean;std;amplitude')
                return

            template['G_MEAN'].append(np.float64(str.strip(line[1])))
            template['G_STD'].append(np.float64(str.strip(line[2])))
            template['G_N'].append(np.float64(str.strip(line[3])))
            return
        else:
            print('{}: Not used\n'.format(line[0]))

    f = open(file)
    template['SYNTHETIC'] = 0

    while True:
        line = f.readline()
        if line == "":
            f.close()
            break
        switch(line.split(";"))

    return template


def init(vars_config_json: str):
    env = dotenv_values(".env")

    for key in list(filter(lambda key: 'QDC_2D_DB' in key, env.keys())):
        os_env = os.getenv(key)
        if os_env != None:
            env[key] = os_env

    env_keys: list = list(env.keys())
    for key in env_keys:
        env[key.replace('QDC_2D_', '')] = env.pop(key, None)

    var_config: dict
    if vars_config_json == None:
        var_config = json.load(open(os.getcwd() + '/TEMPLATES/TEMPLATE.json'))
    else:
        var_config = json.loads(vars_config_json)

    config = var_config | env

    return config
