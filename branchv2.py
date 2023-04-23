class Item:
    def __init__(self, _w: float, _v: int, _c: int, _idx: int):
        self.weight = _w
        self.value = _v
        self.label = _c
        self.index = _idx
        self.ratio = _v / _w


class Node:
    def __init__(self, _i: [], _c, _w: float, _v: int, _idx: int):
        self.items = _i
        self.labels = _c
        self.weight = _w
        self.value = _v
        self.index = _idx


class Knapsack:
    def __init__(self, case):
        self.capacity = case["capacity"]
        self.number_of_classes = case["number_of_classes"]
        self.items = [
            Item(case["weights"][i], case["values"][i], case["labels"][i], i) for i in range(len(case["weights"]))
        ]
        # self.items = _i
        self.items.sort(key=lambda x: x.ratio, reverse=True)

    def isPromising(self, node: Node, capacity: int, best_value: int) -> bool:
        return node.weight <= capacity and self.bound(node) > best_value

    def bound(self, node: Node) -> float:
        if node.index == len(self.items):
            return node.value
        return self.items[node.index].ratio * (self.capacity - node.weight) + node.value

    def class_check(self, node: Node) -> bool:
        return len(node.labels) == self.number_of_classes

    def solve(self):
        best_value = 0
        queue = [Node([], set(), 0, 0, 0)]
        ans = []
        while queue:
            # print(best_value)
            node = queue.pop()
            i = node.index
            if i == len(self.items):
                if (
                    len(node.labels) == self.number_of_classes
                    and node.weight <= self.capacity
                    and node.value > best_value
                ):
                    best_value = node.value
                    # if best_value == node.value:
                    #     pass
                    ans = [x.index for x in node.items]
                    continue
            else:
                item = self.items[i]
                new_labels = set()
                new_labels = node.labels.copy()
                new_labels.add(item.label)
                print(new_labels)
                with_item = Node(
                    node.items + [item],
                    new_labels,
                    node.weight + item.weight,
                    node.value + item.value,
                    node.index + 1,
                )
                without_item = Node(node.items, node.labels, node.weight, node.value, node.index + 1)
                if self.isPromising(with_item, self.capacity, best_value):
                    queue.append(with_item)
                if self.isPromising(without_item, self.capacity, best_value):
                    queue.append(without_item)
        return best_value, ans


def run(case):
    ks = Knapsack(case)
    return ks.solve()
