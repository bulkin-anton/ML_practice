import numpy as np


def euclidean_distance(X, Y):
    X_sqr = np.sum(X ** 2, axis=1)[:, np.newaxis]
    Y_sqr = np.sum(Y ** 2, axis=1)
    return np.sqrt(X_sqr + Y_sqr - 2 * np.dot(X, Y.T))


def cosine_distance(X, Y):
    dot_product = X @ Y.T
    lin_norms_product = (np.sqrt(np.sum(X ** 2, axis=1))[:, np.newaxis] @
                         np.sqrt(np.sum(Y ** 2, axis=1)).T[np.newaxis, :])
    return 1 - (dot_product / lin_norms_product)
