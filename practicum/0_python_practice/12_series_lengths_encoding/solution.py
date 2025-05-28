import numpy as np


def encode_rle(x):
    diffs = np.where(np.diff(x) != 0)[0] + 1
    values = x[diffs - 1]
    values = np.concatenate((values, np.array([x[-1]])))
    pos = np.concatenate((np.array([0]), diffs,
                          np.array([x.shape[0]])))
    pos = np.diff(pos)
    return (values, pos)
