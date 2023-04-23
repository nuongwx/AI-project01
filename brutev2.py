def countUnique(list):
    tmp_set = set(list)
    return len(tmp_set)


class BruteForce:
    def __init__(self, case):
        # self.capacity, self.num_class, self.weights, self.values, self.labels = readfile(id)
        self.capacity = case["capacity"]
        self.num_class = case["number_of_classes"]
        self.weights = case["weights"]
        self.values = case["values"]
        self.labels = case["labels"]
        self.highest_val = 0
        self.best_track = []
        self.best_value = 0

    def Brute(self):
        track = []
        track_labels = []
        index = 0

        self.algorithm(track, track_labels, index)

    def algorithm(self, track, track_labels, index):
        if index == len(self.labels):
            if countUnique(track_labels) != self.num_class:
                return

            calW = 0
            calValue = 0

            for i in range(len(self.labels)):
                calW += self.weights[i] * track[i]
                calValue += self.values[i] * track[i]

            # print(calW, calValue)

            if calValue > self.best_value and calW <= self.capacity:
                self.best_value = calValue
                self.best_track = track.copy()
            return

        for i in range(2):
            track.append(i)

            if i == 1:
                track_labels.append(self.labels[index])

            self.algorithm(track, track_labels, index + 1)

            track.pop(-1)
            if i == 1:
                track_labels.pop(-1)


def run(case):
    brute = BruteForce(case)
    brute.Brute()
    return brute.best_value, brute.best_track
