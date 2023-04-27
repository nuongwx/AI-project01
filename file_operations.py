def read_file(filename):
    with open(filename, "r") as f:
        temp = {"capacity": 0, "number_of_classes": 0, "weights": [], "values": [], "labels": []}
        try:
            temp = {
                "capacity": float(f.readline()),
                "number_of_classes": int(f.readline()),
                "weights": [float(x) for x in f.readline().split(",")],
                "values": [int(x) for x in f.readline().split(",")],
                "labels": [int(x) for x in f.readline().split(",")],
            }
        except ValueError or len(temp["weights"]) != len(temp["values"]) or len(temp["labels"]) != len(temp["values"]):
            print("\033[H\033[J")
            print(filename + " is invalid")
        return temp


def write_file(filename, val, ans):
    with open(filename, "w") as f:
        f.write(str(val) + "\n")
        f.write(", ".join([str(x) for x in ans]))
