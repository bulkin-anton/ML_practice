class WordContextGenerator:
    def __init__(self, word, k):
        self.words = word
        self.window = k

    def __iter__(self):
        for i in range(len(self.words)):
            for j in range(max(0, i - self.window),
                           min(len(self.words), i + self.window + 1)):
                if (i != j):
                    yield self.words[i], self.words[j]
