import random


class Node:
    def __init__(self, id, weight, value, label):
        self.i, self.w, self.v, self.l = id, weight, value, label

    def __str__(self):
        return f"(w = {self.w}, v = {self.v}, l = {self.l})"


class LocalBeam:
    def __init__(self, case):
        # self.capacity, self.num_class, self.weights, self.values, self.labels = readfile(id)
        self.capacity = case["capacity"]
        self.num_class = case["number_of_classes"]
        self.weights = case["weights"]
        self.values = case["values"]
        self.labels = case["labels"]
        self.highest_val = 0

    def add_random(self, track):
        n = len(self.values)
        while True:
            idx = random.randint(0, n - 1)
            if track[idx] == 0:
                track[idx] = 1
                return track

    def algo(self, beam_width=2):
        n = len(self.values)
        paths_so_far = [(tuple(), 0, 0, tuple())]

        for idx in range(n):
            paths_at_tier = []

            for i in range(len(paths_so_far)):
                set_of_items, value, weight, class_set = paths_so_far[i]
                for j in range(n):
                    if j not in set_of_items and weight + self.weights[j] <= self.capacity:
                        # unique indices
                        new_set_of_items = set(set_of_items).copy()
                        new_set_of_items.add(j)
                        new_set_of_items = tuple(new_set_of_items)
                        # and labels set
                        updated_class_set = set(class_set).copy()
                        updated_class_set.add(self.labels[j])
                        updated_class_set = tuple(updated_class_set)

                        path_extended = (
                            new_set_of_items,
                            value + self.values[j],
                            weight + self.weights[j],
                            updated_class_set,
                        )
                    else:
                        path_extended = (set_of_items, value, weight, class_set)
                    paths_at_tier.append(path_extended)
            paths_at_tier.extend
            paths_ordered = sorted(
                paths_at_tier,
                key=lambda element: (len(element[3]), element[1], self.capacity - element[2]),
                reverse=True,
            )
            paths_ordered = list(sorted(set(paths_ordered), key=paths_ordered.index))
            paths_so_far = paths_ordered[:beam_width]

        best_path = paths_so_far[0]
        best_track = [0] * n
        label_set = set()
        total_weight = 0
        for x in best_path[0]:
            best_track[x] = 1
            total_weight += self.weights[x]
            label_set.add(self.labels[x])
        if total_weight > self.capacity or len(label_set) != self.num_class:
            return 0, best_track
        self.highest_val = best_path[1]
        return self.highest_val, best_track


def run(case):
    beam = LocalBeam(case)
    return beam.algo(100)
