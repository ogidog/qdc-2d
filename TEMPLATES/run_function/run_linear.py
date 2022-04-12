def run_linear(template):
    if 'INPUT' in template.keys():
        joint_file = template['INPUT']
    else:
        print('Missing arguments : INPUT (mandatory)')
        return

    info_scanline = {}
    if 'NORTH' in template.keys():
        info_scanline['north'] = template['NORTH']
        print('North orientation given. Joints rotation')
    else:
        info_scanline['north'] = 0

    pass
