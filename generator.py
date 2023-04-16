import random


class Node:
    def __init__(self, weight, value, class_type, ans=0):
        self.weight = weight
        self.value = value
        self.type = class_type
        self.ans = ans

    def __eq__(self, other):
        return (
            self.weight == other.weight
            and self.value == other.value
            and self.type == other.type
        )

    def __lt__(self, other):
        return self.type < other.type


def generate_dataset(size, num_of_class):
    arr = []
    min_weight = max_weight = 0
    for i in range(num_of_class):
        arr.append(
            Node(
                random.random() * random.randint(1, 100),
                random.randint(1, 100),
                i + 1,
                1,
            )
        )
        min_weight += arr[i].weight
    for i in range(size - num_of_class):
        arr.append(
            Node(
                random.random() * random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, num_of_class),
            )
        )
    # max_weight = sum of weight of all items
    max_weight = sum([i.weight for i in arr])
    random.shuffle(arr)
    return (
        random.randint(int(min_weight), int(max_weight)),
        num_of_class,
        arr,
    )


def print_dataset(capacity, num_of_class, dataset, filename="dataset.txt"):
    with open(filename, "w") as file:
        file.write(str(capacity) + "\n")
        file.write(str(num_of_class) + "\n")
        file.write(", ".join([str(i.weight) for i in dataset]) + "\n")
        file.write(", ".join([str(i.value) for i in dataset]) + "\n")
        file.write(", ".join([str(i.type) for i in dataset]) + "\n")
        file.write(", ".join([str(i.ans) for i in dataset]) + "\n")


def verify_answer(file_input="input.txt", file_output="output.txt"):
    # read file input.txt and verify the answer on output.txt
    with open(file_input, "r") as file:
        capacity = int(file.readline())
        num_of_class = int(file.readline())
        weight = [float(x) for x in file.readline().split(",")]
        value = [int(x) for x in file.readline().split(",")]
        label = [int(x) for x in file.readline().split(",")]
    with open(file_output, "r") as file:
        total_value = int(file.readline())
        ans = [int(x) for x in file.readline().split(",")]
    # verify
    total_weight = 0
    existing_class = []
    for i, idx in enumerate(ans):
        total_weight += weight[i] * idx
        if idx == 1:
            existing_class.append(label[i])
    if total_weight > capacity:
        print("total weight > capacity")
        return False
    if len(list(set(existing_class))) != num_of_class:
        print("not enough class")
        return False
    return True


def main():
    capacity, num_of_class, dataset = generate_dataset(20, 5)
    print_dataset(capacity, num_of_class, dataset, "INPUT_" + str(capacity) + ".txt")
    # print(verify_answer())


if __name__ == "__main__":
    main()
