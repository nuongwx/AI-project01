def read_file(filename):
    with open(filename, "r") as f:
        return {
            "capacity": float(f.readline()),
            "number_of_classes": int(f.readline()),
            "weights": [float(x) for x in f.readline().split(",")],
            "values": [int(x) for x in f.readline().split(",")],
            "labels": [int(x) for x in f.readline().split(",")],
        }


def write_file(filename, val, ans):
    with open(filename, "w") as f:
        f.write(str(val) + "\n")
        f.write(", ".join([str(x) for x in ans]))
