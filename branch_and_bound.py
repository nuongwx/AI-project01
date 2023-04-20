class Node:
    def __init__(self, w, v, c, i):
        self.weight = w
        self.value = v
        self.label = c
        self.index = i  # index in the original array since we need to do some sorting
        self.cost = v / w  # idk old man said to do this


class BranchAndBound:
    def __init__(self, case):
        self.upper_bound = 0
        self.answer = []
        self.capacity = case["capacity"]
        self.num_of_class = case["number_of_classes"]
        self.weight = case["weights"]
        self.value = case["values"]
        self.label = case["labels"]
        self.data = list(Node(self.weight[i], self.value[i], self.label[i], i) for i in range(self.weight.__len__()))
        self.zmap = {i: self.data[i] for i in range(len(self.data))}
        self.data.sort(key=lambda x: x.cost, reverse=True)  # prio q

    def print(self):
        return self.upper_bound, self.answer

    def class_check(self, candidate):
        # check whether candidate contains all classes
        classes = set()
        for i, idx in enumerate(candidate):
            if idx == 1:
                classes.add(self.label[i])
        return len(classes) == self.num_of_class

    def run(self):
        candidate = [0] * len(self.data)
        self.solve_branch_and_bound(candidate, 0, self.capacity, 0)
        return self.print()

    def solve_branch_and_bound(self, candidate, depth, remaining_weight, current_value):
        print(self.upper_bound, current_value, remaining_weight)
        for i in range(2):
            candidate[self.data[depth].index] = i
            if i == 1:
                remaining_weight -= self.data[depth].weight
                current_value += self.data[depth].value
            if remaining_weight >= 0:
                if depth == len(self.data) - 1:
                    if current_value > self.upper_bound and self.class_check(candidate):
                        self.upper_bound = current_value
                        self.answer = candidate.copy()
                # textbook heuristic really
                elif current_value + remaining_weight * self.data[depth + 1].cost > self.upper_bound:
                    self.solve_branch_and_bound(candidate, depth + 1, remaining_weight, current_value)
            # if i == 1:    # this is not needed since we are not going to use the candidate # array again
            #     current_weight += self.data[depth].weight
            #     current_value -= self.data[depth].value


def run(case):
    bnb = BranchAndBound(case)
    return bnb.run()
