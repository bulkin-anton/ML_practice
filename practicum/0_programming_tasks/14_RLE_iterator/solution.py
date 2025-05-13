import numpy as np


class RleSequence:
    def __init__(self, input_sequence):
        self.values, self.pos = self._encode_rle(input_sequence)

    def _encode_rle(self, x):
        diffs = np.where(np.diff(x) != 0)[0] + 1
        values = x[diffs - 1]
        values = np.concatenate((values, np.array([x[-1]])))
        pos = np.concatenate((np.array([0]), diffs,
                              np.array([x.shape[0]])))
        pos = np.diff(pos)
        return (values, pos)

    def __cointains__(self, el):
        return el in self.values

    def __iter__(self):
        for value, cnt in zip(self.values, self.pos):
            for i in range(cnt):
                yield value

    def __getitem__(self, index):
        len = self.pos.sum()
        if isinstance(index, int):
            if index < 0:
                index += len
            indexes = np.cumsum(self.pos)
            return self.values[np.searchsorted(indexes, index, side='right')]
        elif isinstance(index, slice):
            start, stop, step = index.indices(len)
            if start >= stop:
                return np.array([])
            indixes = np.arange(start, stop, step)
            counts = np.cumsum(self.pos)
            indexes_found = np.searchsorted(counts, indixes, side='right')
            sliced_values = self.values[indexes_found]
            return sliced_values
