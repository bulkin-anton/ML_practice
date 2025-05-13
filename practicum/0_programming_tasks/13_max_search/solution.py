import numpy as np


def get_max_before_zero(x):
    new_arr = x[1:]
    res = np.where(np.diff(x) == new_arr)[0] + 1
    if (len(res) != 0):
        return x[res].max().item()
    else:
        return None
