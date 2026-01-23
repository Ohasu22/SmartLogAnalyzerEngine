# I searched for other anomaly detection algos
# easiest one was static threshold but its just too simple
# edit: find a algo which could do the job in O(1)
# deep learning is NO my laptop cant handle that so i would give it to a server
# Rolling mean is a good
# time series modal is good
# going with time series YES
#edit: time series complicates things too much, going with rolling mean
# formula = (value - data) / standard deviation
from collections import deque
import math

class RollingStats:
    def __init__(self, window_size, threshold = 2):
        self.window_size = window_size
        self.threshold = threshold
        self.values = deque()
        self.sum = 0.0
        self.sum_square = 0.0


    def update(self, value):
        self.values.append(value)
        self.sum += value
        self.sum_square += value * value

        if len(self.values) > self.window_size:
            old = self.values.popleft()
            self.sum -= old
            self.sum_square -= old * old

    def mean(self):
        # just a fall back for edge cases
        if not self.values:
            return 0
        return self.sum / len(self.values)

    def std(self):
        n = len(self.values)

        if n < 2:
            return 0
        variance = (self.sum_square / n) - (self.mean() ** 2)
        return math.sqrt(max(variance, 0))

    def is_anomaly(self, value):
        if len(self.values) < self.window_size:
            return False
        return value > self.mean() + self.threshold * self.std()