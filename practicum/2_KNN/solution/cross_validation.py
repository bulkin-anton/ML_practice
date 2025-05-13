import numpy as np
from nearest_neighbors import KNNClassifier


def kfold(n, n_folds):
    np.int = int
    indexes = np.random.permutation(np.arange(n))
    fold_sizes = np.full(n_folds, n // n_folds)
    fold_sizes[:n % n_folds] += 1
    points = np.cumsum(fold_sizes)[:-1]
    folds = np.split(indexes, points)
    return [(np.concatenate(folds[:i] + folds[i+1:]), folds[i])
            for i in range(n_folds)]


def accuracy(y_test, y_pred):
    return np.sum(y_test == y_pred) / len(y_test)


def knn_cross_val_score(X, y, k_list, score, cv=None, **kwargs):
    n = len(y)
    if cv is None:
        cv = kfold(n, 5)
    scores = {k: np.zeros(len(cv)) for k in k_list}
    model = KNNClassifier(k=max(k_list), **kwargs)
    for i, (train, test) in enumerate(cv):
        X_train, y_train = X[train], y[train]
        X_test, y_test = X[test], y[test]
        model.fit(X_train, y_train)
        dists, knns = model.find_kneighbors(X_test, return_distance=True)
        s_train = y_train[knns]
        for k in k_list:
            dists_k = dists[:, :k]
            s_k = s_train[:, :k]
            classified = np.zeros(len(s_train))
            for index, s_y in enumerate(s_k):
                if model.weights:
                    weights = (1 / (dists_k[index] + 10 ** (-5)))
                else:
                    weights = np.ones(dists_k[index].shape)
                state = np.bincount(s_y, weights=weights)
                classified[index] = np.argmax(state)
            if (score == 'accuracy'):
                scores[k][i] = accuracy(y_test, classified)
    return scores
