import numpy as np


def mean_orientation(nodes):
    orientations = {}

    ori_vect = nodes['ori_mean_deg']
    orientations['MEAN'] = np.mean(ori_vect)
    orientations['STD'] = np.std(ori_vect)
    orientations['MIN'] = np.min(ori_vect)
    orientations['MAX'] = np.max(ori_vect)

    # add complementary values
    ori_vect = np.array(ori_vect)
    ori_vect_all = np.vstack((ori_vect, ori_vect + 180))

    ori_vect_perp = ori_vect_all[np.where(ori_vect_all > 90)]
    ori_vect_perp = ori_vect_perp[np.where(ori_vect_perp < 270)]
    MEAN_perp = np.mean(ori_vect_perp)
    STD_perp = np.std(ori_vect_perp)

    if STD_perp < orientations['STD'] / 5:  # ori close to 0 or 180
        orientations['MEAN'] = MEAN_perp
        orientations['STD'] = STD_perp
        orientations['MIN'] = np.min(ori_vect_perp)
        orientations['MAX'] = np.max(ori_vect_perp)

    return orientations
