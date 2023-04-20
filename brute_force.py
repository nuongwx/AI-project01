class BruteForce:
    def __init__(self, case):
        self.capacity = case["capacity"]
        self.number_of_classes = case["number_of_classes"]
        self.weights = case["weights"]
        self.values = case["values"]
        self.labels = case["labels"]
        self.highestVal = 0

    def run(self):
        track = [0] * len(self.labels)
        best_track = [0] * len(self.labels)
        calW, calValue, index = 0, 0, 0
        best_track = self.bruteForce(0, track, best_track, calW, calValue, index)
        return self.highestVal, best_track

    def bruteForce(self, count_class, track, best_track, calW, calValue, index):
        print(self.highestVal)
        count_class = len(set(self.labels[i] for i in range(len(self.labels)) if track[i] == 1))
        if calValue > self.highestVal and count_class == self.number_of_classes:
            self.highestVal = calValue
            best_track = track[:]  # copy member

        if index == len(self.weights) or calW > self.capacity:
            return best_track

        if calW + self.weights[index] <= self.capacity:
            track[index] = 1
            best_track = self.bruteForce(
                count_class,
                track,
                best_track,
                calW + self.weights[index],
                calValue + self.values[index],
                index + 1,
            )
            track[index] = 0

        best_track = self.bruteForce(count_class, track, best_track, calW, calValue, index + 1)
        return best_track


def run(case):
    bfs = BruteForce(case)
    return bfs.run()
