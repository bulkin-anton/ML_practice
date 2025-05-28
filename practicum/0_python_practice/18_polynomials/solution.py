class Polynomial:
    def __init__(self, *args):
        self.__dict__['coefs'] = list(args)

    def __call__(self, point):
        res = 0
        x = 1
        for pow, coef in enumerate(self.coefs):
            if (pow != 0):
                x *= point
            res += coef * x
        return res

    def __setattr__(self, key, value):
        if key == 'coefs':
            if isinstance(value, (tuple, list)):
                self.__dict__['coefs'] = list(value)
            else:
                raise TypeError
        else:
            self.__dict__[key] = value

    def __getitem__(self, item):
        return self.coefs[item]

    def __setitem__(self, key, value):
        self.coefs[key] = value


class IntegerPolynomial(Polynomial):
    def __init__(self, *args):
        self.__dict__['coefs'] = [int(round(x)) for x in args]

    def __setattr__(self, key, value):
        if key == 'coefs':
            if isinstance(value, (tuple, list)):
                self.__dict__['coefs'] = [int(round(x)) for x in value]
            else:
                raise TypeError
        else:
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.coefs[key] = int(round(value))
        else:
            self.coefs[key] = [int(round(x)) for x in value]
