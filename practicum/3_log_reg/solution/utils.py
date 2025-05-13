import numpy as np


def grad_finite_diff(function, w, eps=1e-8):
    function_vctr = np.vectorize(function, signature='(n)->()')
    matr_w = np.tile(w, (len(w), 1))
    matr_e = np.eye(len(w)) * eps
    return (function_vctr(matr_w + matr_e) - function_vctr(matr_w)) / eps
