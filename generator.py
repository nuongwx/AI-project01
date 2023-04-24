import random


class Node:
    def __init__(self, weight, value, class_type, ans=0):
        self.weight = weight
        self.value = value
        self.type = class_type
        self.ans = ans


def generate_dataset(size, num_of_class):
    arr = []
    min_weight = max_weight = 0
    for i in range(num_of_class):
        arr.append(
            Node(
                random.gauss(10, 1) * random.randint(1, 10),
                random.randint(1, 10),
                i + 1,
                1,
            )
        )
        min_weight += arr[i].weight
    for i in range(size - num_of_class):
        arr.append(
            Node(
                random.gauss(10, 1) * random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, num_of_class),
            )
        )
    max_weight = sum([i.weight for i in arr])
    random.shuffle(arr)
    return (
        # random.randint(int(min_weight), max(int(min_weight), int((max_weight + min_weight) / 4))),
        int(min_weight + 0.1 * min_weight),  # deterministic?
        num_of_class,
        arr,
    )


def print_dataset(capacity, num_of_class, dataset, filename="dataset.txt"):
    with open(filename, "w") as file:
        file.write(str(capacity) + "\n")
        file.write(str(num_of_class) + "\n")
        file.write(", ".join([str(i.weight) for i in dataset]) + "\n")
        file.write(", ".join([str(i.value) for i in dataset]) + "\n")
        file.write(", ".join([str(i.type) for i in dataset]) + "\n\n")
        # some statistics
        file.write("Size: " + str(len(dataset)) + "\n")
        file.write("Weight: " + str(sum([i.weight for i in dataset])) + "\n")
        file.write(", ".join([str(i.ans) for i in dataset]) + "\n")


def verify_answer(file_input="input.txt", file_output="output.txt"):
    # read file input.txt and verify the answer on output.txt
    with open(file_input, "r") as file:
        capacity = float(file.readline())
        num_of_class = int(file.readline())
        weight = [float(x) for x in file.readline().split(",")]
        value = [int(x) for x in file.readline().split(",")]
        label = [int(x) for x in file.readline().split(",")]
    with open(file_output, "r") as file:
        solution_value = int(file.readline())
        ans = [int(x) for x in file.readline().split(",")]
    # verify
    total_weight = 0
    total_value = 0
    existing_class = []
    for i, idx in enumerate(ans):
        total_weight += weight[i] * idx
        total_value += value[i] * idx
        if idx == 1:
            existing_class.append(label[i])
    if total_weight > capacity:
        print("total weight > capacity")
        print(total_weight, capacity)
        # return False
    if solution_value != total_value:
        print("solution value != total value")
        print(solution_value, total_value)
        # return False
    if len(list(set(existing_class))) != num_of_class:
        print("not enough class")
        print(len(list(set(existing_class))), num_of_class)
        # return False
    print("OK")
    # return True


def main():
    # capacity, num_of_class, dataset = generate_dataset(50, 5)
    # print_dataset(capacity, num_of_class, dataset, "test" + str(capacity) + ".txt")
    # print(verify_answer("test/ptn.txt", "test/output.txt"))
    size = [10, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    n_class = [1, 2, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(size)):
        capacity, num_of_class, dataset = generate_dataset(size[i], n_class[i])
        print_dataset(capacity, num_of_class, dataset, f"test/input/INPUT_{i + 1}.txt")


if __name__ == "__main__":
    main()
