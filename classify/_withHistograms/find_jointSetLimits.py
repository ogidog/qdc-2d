import numpy as np
from scipy.optimize import fmin
from scipy.stats import norm
import utils.lang as lang
import workflow.workflow_config as wfc


def equation2solve(x, gaussians_params, gauss):
    return np.abs(
        gaussians_params[gauss + 1][2] * norm.pdf(x, gaussians_params[gauss + 1][0], gaussians_params[gauss + 1][1]) -
        gaussians_params[gauss][2] * norm.pdf(x, gaussians_params[gauss][0], gaussians_params[gauss][1]))


def find_jointSetLimits(gaussian_params):
    nbJointsSet = gaussian_params['NBjointSet']
    G_mean = gaussian_params['G_mean']
    G_std = gaussian_params['G_std']
    G_N = gaussian_params['G_N']

    if len(G_mean) <= 1:  # only on joint set, no intersection
        intersection = -1
    else:
        w = np.array([G_mean, G_std, G_N]).T.tolist()
        intersection = np.zeros(nbJointsSet)
        gaussians_params = sorted(w)

        for gauss in range(len(intersection) - 1):
            # define equation to minimize and to solve
            equation2solve = lambda x: np.abs(
                gaussians_params[gauss + 1][2] * norm.pdf(x, gaussians_params[gauss + 1][0],
                                                          gaussians_params[gauss + 1][1])
                - gaussians_params[gauss][2] * norm.pdf(x, gaussians_params[gauss][0], gaussians_params[gauss][1]))
            inter = fmin(equation2solve, (gaussians_params[gauss][0] + gaussians_params[gauss + 1][0]) / 2, disp=False)
            intersection[gauss] = inter

        # equation to solve for the intersection of first and last gaussians
        equation2solve = lambda x: np.abs(
            gaussians_params[-1][2] * norm.pdf(x, gaussians_params[-1][0], gaussians_params[-1][1]) -
            gaussians_params[0][2] * norm.pdf(x, gaussians_params[0][0] + 180, gaussians_params[0][1]))
        inter = fmin(equation2solve, (gaussians_params[-1][0] + gaussians_params[0][0] + 180) / 2, disp=False)
        intersection[-1] = inter
        # rescale intersection to have between (0-180)
        intersection[intersection > 180] = intersection[intersection > 180] - 180
        intersection[intersection < 0] = intersection[intersection < 0] + 180

        # Sorting results and resume
        intersection = sorted(intersection)
        print(lang.select_locale('The classification limits are : {}',
                                 'Ограничения классификации : {}').format(intersection))
        wfc.optimization_brief[
            lang.select_locale('The classification limits are', 'Ограничения классификации')] = intersection

    return intersection
