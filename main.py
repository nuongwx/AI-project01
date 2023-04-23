import timeit
import os

from generator import main as generate_dataset

# import memory_profiler as mem_profile
# import csv
import file_operations as fo

# import brute_force as bf.old
import brutev2 as bf

import branch_and_bound as br

# import branchv2 as br2

import beam as bm

import genetic_algorithms as ga


def main():
    # generate_dataset()
    a_name = ["Brute Force", "Branch and Bound", "Beam", "Genetic Algorithms"]
    fp = [bf.run, br.run, bm.run, ga.run]
    with open("results.csv", "w+") as f:
        for idx, i in enumerate(fp):
            print(f"Running {a_name[idx]}")
            f.write(f"{a_name[idx]}, ")
            for j in range(1, 10):
                print(f"Case {j}")
                case = fo.read_file(f"test/input/INPUT_{j}.txt")
                start = timeit.default_timer()
                # mem1 = mem_profile.memory_usage()
                val, ans = i(case)
                # mem2 = mem_profile.memory_usage()
                stop = timeit.default_timer()
                fo.write_file(f"test/output/{a_name[idx]}/OUTPUT_{j}.txt", val, ans)
                # writer.writerow(["", stop - start, mem2[0] - mem1[0]])
                f.write(f"{stop - start}, ")
                f.flush()
                os.fsync(f.fileno())
            f.write("\n")


if __name__ == "__main__":
    main()
