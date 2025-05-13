import numpy as np
import time
from oracles import BinaryLogistic
from scipy.special import expit
from scipy.sparse import csr_matrix


class GDClassifier:

    def __init__(
        self, loss_function, step_alpha=1, step_beta=0,
        tolerance=1e-5, max_iter=1000, **kwargs
    ):
        if loss_function == 'binary_logistic':
            self.loss = BinaryLogistic(**kwargs)
        else:
            raise ValueError
        self.step_alpha = step_alpha
        self.step_beta = step_beta
        self.tolerance = tolerance
        self.max_iter = max_iter

    def fit(self, X, y, w_0=None, trace=False, X_test=None, y_test=None):
        if w_0 is not None:
            self.weights = w_0.copy()
        else:
            self.weights = np.zeros(X.shape[1])
        history = {}
        history['time'] = [0.0]
        history['func'] = [self.loss.func(X, y, self.weights)]
        history['accur'] = [0.0]
        for k in range(1, self.max_iter + 1):
            start_time = time.time()
            gw = self.loss.grad(X, y, self.weights)
            eta = self.step_alpha / (k ** self.step_beta)
            self.weights = self.weights - eta * gw
            func_res = self.loss.func(X, y, self.weights)
            if abs(func_res - history['func'][-1]) < self.tolerance:
                stop_time = time.time()
                history['func'].append(func_res)
                history['time'].append(stop_time - start_time)
                if (X_test is not None) and (y_test is not None):
                    accuracy = self.get_accuracy_score(self.predict(X_test),
                                                       y_test)
                    history['accur'].append(accuracy)
                break
            stop_time = time.time()
            history['func'].append(func_res)
            history['time'].append(stop_time - start_time)
            if (X_test is not None) and (y_test is not None):
                accuracy = self.get_accuracy_score(self.predict(X_test),
                                                   y_test)
                history['accur'].append(accuracy)
        if trace:
            return history

    def predict(self, X):
        return np.where(X.dot(self.weights) > 0, 1, -1)

    def predict_proba(self, X):
        sigm = np.array(expit(np.dot(self.weights, X.T)))
        ans = np.empty((2, len(X)))
        ans[0] = sigm
        ans[1] = 1 - sigm
        return ans

    def get_objective(self, X, y):
        return self.loss.func(X, y, self.weights)

    def get_gradient(self, X, y):
        return self.loss.grad(X, y, self.weights)

    def get_weights(self):
        return self.weights

    def get_accuracy_score(self, y_pred, y_true):
        return np.sum(y_pred == y_true) / len(y_true)


class SGDClassifier(GDClassifier):

    def __init__(
        self, loss_function, batch_size, step_alpha=1, step_beta=0,
        tolerance=1e-5, max_iter=1000, random_seed=153, **kwargs
    ):
        super().__init__(loss_function, step_alpha, step_beta, tolerance,
                         max_iter, **kwargs)
        self.random_seed = random_seed
        self.batch_size = batch_size

    def fit(self, X, y, w_0=None, trace=False,
            log_freq=1, X_test=None, y_test=None):
        np.random.seed(self.random_seed)
        if w_0 is not None:
            self.weights = w_0.copy()
        else:
            self.weights = np.zeros(X.shape[1])
        history = {}
        history['time'] = [0.0]
        history['func'] = [self.loss.func(X, y, self.weights)]
        history['epoch_num'] = [0.0]
        history['weights_diff'] = [0.0]
        history['accur'] = [0.0]
        prev_loss = history['func'][-1]
        prev_epoch = 0
        start_time = time.time()
        for k in range(1, self.max_iter + 1):
            epoch = (k + 1) * self.batch_size / X.shape[0]
            batch = np.random.randint(0, X.shape[0], self.batch_size)
            gw = self.loss.grad(X[batch], y[batch], self.weights)
            eta = self.step_alpha / ((epoch + 1) ** self.step_beta)
            prev_weights = self.weights
            self.weights -= eta * gw
            if epoch - prev_epoch > log_freq:
                end_time = time.time()
                history['func'].append(self.loss.func(X, y, self.weights))
                history['epoch_num'].append(epoch)
                history['weights_diff'].append(np.sum(
                    (self.weights - prev_weights) ** 2)
                )
                if X_test is not None:
                    history['accur'].append(
                        self.get_accuracy_score(self.predict(X_test), y_test))
                history['time'].append(end_time - start_time)
                start_time = end_time
                if abs(history['func'][-1] -
                       history['func'][-2]) < self.tolerance:
                    break
        if trace:
            return history
