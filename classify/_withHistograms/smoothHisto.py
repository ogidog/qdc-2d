import numpy as np
from scipy import ndimage


def smoothHisto(data, windowSize):
    smoothed = ndimage.gaussian_filter(data,sigma=1.55)
    return smoothed
