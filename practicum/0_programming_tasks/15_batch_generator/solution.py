import numpy as np


class BatchGenerator:
    def __init__(self, list_of_sequences, batch_size, shuffle=False):
        self.list_of_sequences = list_of_sequences
        self.batch_size = batch_size
        self.seq_length = len(list_of_sequences[0])
        self.indexes = np.arange(self.seq_length)
        if shuffle:
            np.random.shuffle(self.indexes)

    def __iter__(self):
        for start_index in range(0, self.seq_length, self.batch_size):
            end_index = min(start_index + self.batch_size, self.seq_length)
            batch_indixes = self.indexes[start_index:end_index]
            batch = []
            for seq in self.list_of_sequences:
                batch_seq = [seq[i] for i in batch_indixes]
                batch.append(batch_seq)
            yield batch
