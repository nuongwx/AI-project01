import timeit
import os

from generator import main as generate_dataset

# import memory_profiler as mem_profile
import file_operations as fo

import brute_force as bf_old
import brutev2 as bf

# import branch_and_bound as br_old
import branchv2 as br

import beam as bm

import genetic_algorithms as ga


def main():
    # generate_dataset()
    a_name = ["Brute Force", "Branch and Bound", "Beam Search", "Genetic Algorithms"]
    fp = [bf.run, br.run, bm.run, ga.run]
    with open("results.csv", "w+") as f:
        for idx, i in enumerate(fp):
            print(f"Running {a_name[idx]}")
            f.write(f"{a_name[idx]}, ")
            for j in range(0, 10):
                print(f"Case {j + 1}")
                case = fo.read_file(f"test/input/INPUT_{j + 1}.txt")
                start = timeit.default_timer()
                # mem1 = mem_profile.memory_usage()
                val, ans = i(case)
                # mem2 = mem_profile.memory_usage()
                stop = timeit.default_timer()
                fo.write_file(f"test/output/{a_name[idx]}/OUTPUT_{j + 1}.txt", val, ans)
                # writer.writerow(["", stop - start, mem2[0] - mem1[0]])
                f.write(f"{stop - start}, ")
                f.flush()
                os.fsync(f.fileno())
            f.write("\n")


def unit(filename, algo):
    case = fo.read_file(f"{filename}")
    start = timeit.default_timer()
    val, ans = algo.run(case)
    stop = timeit.default_timer()
    print(stop - start)
    print(val, ans)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main()
    # unit("test/input/stuck.txt", br)
