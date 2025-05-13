import numpy as np


def get_nonzero_diag_product(X):
    mul_result = 1
    diag_els = X.diagonal()
    non_zero_elemnts = diag_els[np.where(diag_els != 0)]
    if non_zero_elemnts.size == 0:
        return None
    else:
        return np.prod(non_zero_elemnts).item()
