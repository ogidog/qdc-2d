def find_jointSetLimits(gaussian_params):
    nbJointsSet = gaussian_params['NBjointSet']
    G_mean = gaussian_params['G_mean']
    G_std  = gaussian_params['G_std']
    G_N    = gaussian_params['G_N']

    return intersection