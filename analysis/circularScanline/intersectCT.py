import numpy as np


def intersectCT(x_1, x_2, y_1, y_2, r, lT, xTC, yTC, k, _int):
    dx = x_2 - x_1
    dy = y_2 - y_1

    d = np.sqrt(dx ** 2 + dy ** 2);  # distance
    D = x_1 * y_2 - x_2 * y_1;  # determinant
    x = (D * dy + _int * np.sign(dy) * dx * np.emath.sqrt((r ** 2) * (d ** 2) - D ** 2)) / (d ** 2)
    y = (-D * dx + _int * np.abs(dy) * np.emath.sqrt((r ** 2) * (d ** 2) - (D ** 2))) / d ** 2

    # CHECK IF xTC ON THE JOINTS
    for i in range(len(lT)):
        if np.isreal(x[i]):
            # distance intersection point/middle of segment
            d = np.sqrt(
                (np.real(x[i]) - np.mean([x_2[i], x_1[i]])) ** 2 + (np.real(y[i]) - np.mean([y_2(i), y_1(i)])) ** 2)
            if (d < 0.5 * lT[i]):  # the intersection point is on the segment
                xTC[k] = np.real(x[i])
                yTC[k] = np.real(y[i])
                k = k + 1

    return [xTC, yTC, k]
