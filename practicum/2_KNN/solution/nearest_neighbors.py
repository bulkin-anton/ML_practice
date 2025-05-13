import numpy as np
from sklearn.neighbors import NearestNeighbors
from distances import euclidean_distance, cosine_distance


class KNNClassifier:
    def __init__(self, k, strategy, metric, weights, test_block_size=100):
        self.k = k
        self.strategy = strategy
        if ((self.strategy in ['kd_tree', 'ball_tree']) and
           (metric == 'cosine' or callable(metric))):
            raise TypeError
        self.metric = metric
        self.weights = weights
        self.test_block_size = test_block_size
        self.epsilon = 10 ** (-5)

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        if self.strategy != 'my_own':
            self.neighbors = NearestNeighbors(n_neighbors=self.k,
                                              algorithm=self.strategy,
                                              metric=self.metric)
            self.neighbors.fit(X)

    def _compute_neigh_dists(self, X):
        if self.metric == 'euclidean':
            return euclidean_distance(X, self.X_train)
        elif self.metric == 'cosine':
            return cosine_distance(X, self.X_train)
        else:
            raise TypeError

    def find_kneighbors(self, X, return_distance=True):
        if self.strategy != 'my_own':
            return self.neighbors.kneighbors(X=X,
                                             return_distance=return_distance)
        else:
            distances = self._compute_neigh_dists(X)
            k_nearest = np.argpartition(distances, np.arange(self.k),
                                        axis=1)[:, :self.k]
            if return_distance:
                return distances[np.arange(distances.shape[0])[:, None],
                                 k_nearest], k_nearest
            else:
                return k_nearest

    def predict(self, X):
        distances, indexes = self.find_kneighbors(X, return_distance=True)
        if self.weights:
            weights = 1 / (distances + self.epsilon)
        else:
            weights = np.ones((X.shape[0], self.k))
        neighbors = self.y_train[indexes]
        predictions = np.zeros(neighbors.shape[0])
        for i, neighbor_labels in enumerate(neighbors):
            class_count = np.bincount(neighbor_labels, weights=weights[i])
            predictions[i] = np.argmax(class_count)
        return predictions
