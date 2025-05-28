import numpy as np
import warnings
warnings.filterwarnings('ignore')


def replace_nan_to_means(X):
    matrix = X.copy()
    nan_indexes = np.where(np.isnan(matrix))
    means = np.nanmean(matrix, axis=0)
    means = np.where(np.isnan(means), 0, means)
    matrix[nan_indexes] = means[nan_indexes[1]]
    return matrix
