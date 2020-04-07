class LineReader:
    def __init__(self, filename):
        self.idx = 0
        with open(filename) as f:
            self.lines = f.readlines()

    def next(self):
        line = self.lines[self.idx]
        self.idx += 1
        return line

    def peek(self):
        return self.lines[self.idx + 1]

    def cur(self):
        return self.lines[self.idx]

    def eof(self):
        return self.idx + 1 == len(self.lines) #self.lines[self.idx] == None
