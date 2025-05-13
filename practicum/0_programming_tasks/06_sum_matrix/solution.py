class CooSparseMatrix:
    def __init__(self, ijx_list, shape):
        ijx_list = sorted(ijx_list)
        self.matrix = {}
        self.shape = shape
        for element in ijx_list:
            if not (isinstance(element, tuple)):
                raise TypeError
            if (len(element) != 3):
                raise TypeError
            i, j, x = element
            if not (isinstance(i, int) & isinstance(j, int) &
                    (isinstance(x, float) | isinstance(x, int))):
                raise TypeError
            if ((0 > i) or (i >= shape[0])):
                raise TypeError
            if ((0 > j) or (j >= shape[1])):
                raise TypeError
            if (i in self.matrix.keys()):
                if (j in self.matrix[i].keys()):
                    raise TypeError
                else:
                    self.matrix[i][j] = float(x)
            else:
                self.matrix[i] = {j: float(x)}

    def __getitem__(self, index):
        if (isinstance(index, int)):
            if ((index < 0) or (index >= self.shape[0])):
                raise TypeError
            if (index in self.matrix.keys()):
                ijxlist = []
                for j in self.matrix[index].keys():
                    ijxlist.append((0, j, self.matrix[index][j]))
                return CooSparseMatrix(ijxlist, (1, self.shape[1]))
            else:
                return CooSparseMatrix([], (1, self.shape[1]))
        elif (isinstance(index, tuple)):
            if (len(index) != 2):
                raise TypeError
            if not (isinstance(index[0], int) & isinstance(index[1], int)):
                raise TypeError
            if ((index[0] < 0) or (index[0] >= self.shape[0])):
                raise TypeError
            if ((index[1] < 0) or (index[1] >= self.shape[1])):
                raise TypeError
            if (index[0] in self.matrix.keys()):
                if (index[1] in self.matrix[index[0]].keys()):
                    return self.matrix[index[0]][index[1]]
            return 0
        else:
            raise TypeError

    def __setitem__(self, index, value):
        if (isinstance(index, tuple)):
            if (len(index) != 2):
                raise TypeError
            if ((index[0] < 0) or (index[0] >= self.shape[0])):
                raise TypeError
            if ((index[1] < 0) or (index[1] >= self.shape[1])):
                raise TypeError
            if (index[0] in self.matrix.keys()):
                if (value != 0):
                    self.matrix[index[0]][index[1]] = float(value)
                else:
                    del self.matrix[index[0]][index[1]]
                    if (len(self.matrix[index[0]]) == 0):
                        del self.matrix[index[0]]
            else:
                if (value != 0):
                    self.matrix[index[0]] = {index[1]: float(value)}
        else:
            raise TypeError

    def __add__(self, other):
        if (self.shape != other.shape):
            raise TypeError
        answer = CooSparseMatrix([], self.shape)
        for i_key in self.matrix.keys():
            for j_key in self.matrix[i_key].keys():
                answer[i_key, j_key] = self.matrix[i_key][j_key]
        for i_key in other.matrix.keys():
            for j_key in other.matrix[i_key].keys():
                answer[i_key, j_key] = (answer[i_key, j_key] +
                                        other.matrix[i_key][j_key])
        return answer

    def __sub__(self, other):
        if (self.shape != other.shape):
            raise TypeError
        answer = CooSparseMatrix([], self.shape)
        for i_key in self.matrix.keys():
            for j_key in self.matrix[i_key].keys():
                answer[i_key, j_key] = self.matrix[i_key][j_key]
        for i_key in other.matrix.keys():
            for j_key in other.matrix[i_key].keys():
                answer[i_key, j_key] = (answer[i_key, j_key] -
                                        other.matrix[i_key][j_key])
        return answer

    def __mul__(self, num):
        if not (isinstance(num, int) | isinstance(num, float)):
            raise TypeError
        if (num == 0):
            return CooSparseMatrix([], self.shape)
        ijx_list = []
        for i_key in self.matrix.keys():
            for j_key in self.matrix[i_key].keys():
                ijx_list.append((i_key, j_key,
                                 self.matrix[i_key][j_key] * num))
        return CooSparseMatrix(ijx_list, self.shape)

    def __rmul__(self, num):
        if not (isinstance(num, int) | isinstance(num, float)):
            raise TypeError
        if (num == 0):
            return CooSparseMatrix([], self.shape)
        ijx_list = []
        for i_key in self.matrix.keys():
            for j_key in self.matrix[i_key].keys():
                ijx_list.append((i_key, j_key,
                                 self.matrix[i_key][j_key] * num))
        return CooSparseMatrix(ijx_list, self.shape)


def to_array(matrix: CooSparseMatrix):
    matr = []
    for i in range(matrix.shape[0]):
        if (i in matrix.matrix.keys()):
            row = []
            for j in range(matrix.shape[1]):
                if (j in matrix.matrix[i].keys()):
                    row.append(matrix.matrix[i][j])
                else:
                    row.append(float(0))
        else:
            row = [0.] * matrix.shape[0]
        matr.append(row)
    return matr
