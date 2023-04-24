import heapq


class Item:
    def __init__(self, _w: float, _v: int, _c: int, _idx: int):
        self.weight = _w
        self.value = _v
        self.label = _c
        self.index = _idx
        self.ratio = _v / _w


class Node:
    def __init__(self, _i: list[Item], _c: set, _w: float, _v: int, _idx: int):
        self.items = _i
        self.labels = _c
        self.weight = _w
        self.value = _v
        self.depth = _idx


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.index = 0

    def push(self, _i, priority):
        # -priority makes the pop() method return the item with the highest priority.
        # index is just icing on the cake really, but try to remove it and see what happens
        heapq.heappush(self.queue, (-priority, self.index, _i))
        self.index += 1

    def pop(self) -> Node:
        return heapq.heappop(self.queue)[-1]

    def __len__(self) -> int:
        return len(self.queue)


class Knapsack:
    def __init__(self, case):
        self.capacity = case["capacity"]
        self.number_of_classes = case["number_of_classes"]
        self.items = [
            Item(case["weights"][i], case["values"][i], case["labels"][i], i) for i in range(len(case["weights"]))
        ]
        self.items.sort(key=lambda x: x.ratio, reverse=True)

    def bound(self, node: Node) -> float:
        remaining_capacity = self.capacity - node.weight
        # idx = len(node.items)
        if remaining_capacity < 0:  # = or not =, that's the question
            return 0
        # bound = node.value + self.items[len(node.items)].ratio * remaining_capacity
        result = node.value
        for i in range(node.depth + 1, len(self.items)):
            if self.items[i].weight <= remaining_capacity:
                result += self.items[i].value
                remaining_capacity -= self.items[i].weight
            else:
                result += self.items[i].ratio * remaining_capacity
                break
        return result

    def solve(self) -> tuple[int, list[int]]:
        best_value = 0
        ans = []
        queue = PriorityQueue()
        queue.push(Node([], set(), 0, 0, -1), 0)
        while queue:
            node = queue.pop()
            if node.depth + 1 == len(self.items):
                if (
                    node.weight <= self.capacity
                    and node.value > best_value
                    and len(node.labels) == self.number_of_classes
                ):
                    best_value = node.value
                    # print(best_value)
                    ans = [x.index for x in node.items]
            else:
                item = self.items[node.depth + 1]

                # branching: with item
                new_labels = node.labels.copy()
                new_labels.add(item.label)
                with_item = Node(
                    node.items + [item],
                    new_labels,
                    node.weight + item.weight,
                    node.value + item.value,
                    node.depth + 1,
                )
                with_item_bound = self.bound(with_item)

                # and without item
                without_item = Node(node.items, node.labels, node.weight, node.value, node.depth + 1)
                without_item_bound = self.bound(without_item)

                # the bound part
                if with_item_bound > best_value:
                    queue.push(with_item, with_item_bound)
                if without_item_bound > best_value:
                    queue.push(without_item, without_item_bound)
        return best_value, ans


def run(case):
    ks = Knapsack(case)
    return ks.solve()
