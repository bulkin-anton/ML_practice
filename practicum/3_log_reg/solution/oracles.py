import numpy as np
from scipy.special import expit
from scipy.sparse import csr_matrix


class BaseSmoothOracle:
    """
    Базовый класс для реализации оракулов.
    """
    def func(self, w):
        """
        Вычислить значение функции в точке w.
        """
        if isinstance(self, BinaryLogistic):
            return self.func_res
        raise NotImplementedError('Func oracle is not implemented.')

    def grad(self, w):
        """
        Вычислить значение градиента функции в точке w.
        """
        if isinstance(self, BinaryLogistic):
            return self.grad_res
        raise NotImplementedError('Grad oracle is not implemented.')


class BinaryLogistic(BaseSmoothOracle):
    """
    Оракул для задачи двухклассовой логистической регрессии.

    Оракул должен поддерживать l2 регуляризацию.
    """

    def __init__(self, l2_coef):
        """
        Задание параметров оракула.

        l2_coef - коэффициент l2 регуляризации
        """
        self.l2_coef = l2_coef

    def func(self, X, y, w):
        """
        Вычислить значение функционала в точке w на выборке X с ответами y.

        X - scipy.sparse.csr_matrix или двумерный numpy.array

        y - одномерный numpy array

        w - одномерный numpy array
        """
        if isinstance(X, csr_matrix):
            dot_res = -y * X.dot(w)
        else:
            dot_res = -y * np.dot(X, w)
        function = np.mean(np.logaddexp(0, dot_res))
        l2_function = (self.l2_coef / 2) * np.sum(w * w)
        self.func_res = function + l2_function
        return super().func(w)

    def grad(self, X, y, w):
        """
        Вычислить градиент функционала в точке w на выборке X с ответами y.

        X - scipy.sparse.csr_matrix или двумерный numpy.array

        y - одномерный numpy array

        w - одномерный numpy array
        """
        if isinstance(X, csr_matrix):
            grad = -X.T.dot(y * expit(-y * X.dot(w))) / len(y)
        else:
            grad = -np.dot(X.T, y * expit(-y * np.dot(X, w))) / len(y)
        l2_grad = self.l2_coef * w
        self.grad_res = grad + l2_grad
        return super().grad(w)
