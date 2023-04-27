import os, sys  # path manip, system calls
import timeit, tracemalloc  # measurements

from generator import main as generate_dataset

import file_operations as fo

import brute_force
import branch_and_bound
import local_beam_search
import genetic_algorithms  # algorithms

ALGO_NAME = ["Brute Force", "Branch and Bound", "Beam Search", "Genetic Algorithms"]
ALGO = [brute_force, branch_and_bound, local_beam_search, genetic_algorithms]


def demo():
    # generate_dataset()
    if not os.path.isdir(os.path.normpath(os.getcwd() + "/test/output")):
        os.mkdir(os.path.normpath(os.getcwd() + "/test/output"))
    with open("test/output/stats.csv", "w+") as f:
        f.write("\n")
        for idx, i in enumerate(ALGO):
            clear_screen()
            print(f"Running {ALGO_NAME[idx]}")
            if not os.path.isdir(os.path.normpath(os.getcwd() + f"/test/output/{ALGO_NAME[idx]}")):
                os.mkdir(os.path.normpath(os.getcwd() + f"/test/output/{ALGO_NAME[idx]}"))
            f.write(f"{ALGO_NAME[idx]}, ")
            for j in range(0, 10):
                # print(f"Case {j + 1}")
                # ignore large cases for brute force
                if i == ALGO[0] and j > 3:
                    f.write("-1, -1, ")
                    continue
                #
                val, ans, time, mem = unit(f"test/input/INPUT_{j}.txt", i)
                fo.write_file(f"test/output/{ALGO_NAME[idx]}/OUTPUT_{j}.txt", val, ans)
                f.write(f"{time},{mem}, ")
                f.flush()
                os.fsync(f.fileno())
            f.write("\n")
            input("Press [ENTER] to continue")


def unit(filename, algo):
    try:
        case = fo.read_file(f"{filename}")
    except FileNotFoundError or ValueError:
        print(filename + " is invalid")
        return -1, [], -1
    print("Running " + ALGO_NAME[ALGO.index(algo)] + " on " + filename)
    start = timeit.default_timer()
    tracemalloc.start()
    val, ans = algo.run(case)
    mem = tracemalloc.get_traced_memory()[1] / 1000000
    stop = timeit.default_timer()
    tracemalloc.stop()
    print("Task completed in", stop - start, "seconds")
    print("Memory usage:", mem, "MB")
    print("-" * 42)
    return val, ans, stop - start, mem


def error_message(message, fp):
    print(message)
    print("Press [ENTER] to continue or [CTRL + C] to exit")
    input()
    return fp()


def clear_screen():
    print("\033[H\033[J")


def algorithms_menu():
    clear_screen()
    print("ALGORITHMS")
    print(*[str(i + 1) + ". " + ALGO_NAME[i] for i in range(len(ALGO_NAME))], sep="\n")
    print("0. Exit")
    print("Enter your choice or press [ENTER] run demo: ", end="")
    try:
        text = input()
        if text == "":
            return 0
        choice = int(text)
        if choice == 0:
            clear_screen()
            exit()
        elif choice > 0 and choice <= len(ALGO_NAME):
            return choice
        else:
            raise Exception
    except Exception or ValueError:
        return error_message("Invalid choice. Try again.", algorithms_menu)


def path_clean_and_check(path: str = "", is_folder: bool = False):
    path = path.replace('"', "")
    path = os.path.normpath(path)
    if path.find(os.getcwd()) == -1:
        path = os.path.join(os.getcwd(), path)
    if is_folder:
        if not os.path.isdir(path):
            return error_message("Invalid folder path. Try again.", testcase_source_menu)
    else:
        if not os.path.isfile(path):
            return error_message("Invalid file path. Try again.", testcase_source_menu)
    return path


def testcase_source_menu():
    clear_screen()
    print("INPUT")
    print("1. Input from txt file")
    print("2. Input from folder")
    print("0. Back")
    print("Current working directory: " + os.getcwd())
    print("Enter your choice or press [ENTER] to run defaults: ", end="")
    try:
        text = input()
        if text == "":
            return path_clean_and_check("test/input", True)
        choice = int(text)
        if choice == 0:
            return None
        elif choice == 1:
            print("Enter file path: ", end="")
            return path_clean_and_check(input(), False)
        elif choice == 2:
            print("Enter folder path: ", end="")
            return path_clean_and_check(input(), True)
        else:
            raise Exception

    except Exception or ValueError:
        return error_message("Invalid choice. Try again.", testcase_source_menu)


def boolean_input(msg: str):
    print(msg + " [y/n]: ", end="")
    try:
        text = input()
        if text == "y" or text == "Y" or text == "":
            return True
        elif text == "n" or text == "N":
            return False
        else:
            raise Exception
    except Exception or ValueError:
        return error_message("Invalid choice. Try again.", lambda: boolean_input(msg))


def report_append(filename: str, time: float, mem: float):
    with open("test/output/stats.csv", "a", newline="") as f:
        f.write(f"{filename},{time},{mem}\n")


def menu_handler():
    # invoke algorithms choice menu
    choice = algorithms_menu()
    if choice == 0:
        demo()  # run demo
    # run selected algorithm
    else:
        # invoke input choice menu
        input_path = testcase_source_menu()
        if input_path is None:
            menu_handler()  # backing out
        else:
            val, ans, time, mem = 0, 0, 0, 0

            # creating output necessities
            output_flag = boolean_input("Do you want to save output and stats?")
            if output_flag:
                print("Saving to test/output and stats.csv")
                if not os.path.exists("test/output"):
                    os.mkdir("test/output")
                if not os.path.exists("test/output/" + ALGO_NAME[choice - 1]):
                    os.mkdir("test/output/" + ALGO_NAME[choice - 1])
                if os.path.exists("test/output/stats.csv"):
                    if not boolean_input("stats.csv already exists. Do you want append or overwrite?"):
                        with open("test/output/stats.csv", "w", newline="") as f:
                            f.write("filename,time,mem\n")
            clear_screen()
            try:
                # if input is a folder
                file_list = [os.path.join(input_path, f) for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]  # fmt: skip
                # only run on .txt files
                file_list = [f for f in file_list if f.endswith(".txt")]
                for file in file_list:
                    # print(f"Running {ALGO_NAME[choice - 1]} on {file}")
                    val, ans, time, mem = unit(file, ALGO[choice - 1])
                    if output_flag:
                        report_append(ALGO[choice - 1].__name__ + "," + os.path.basename(file), time, mem)
                        fo.write_file(f"test/output/{ALGO_NAME[choice - 1]}/OUTPUT_{os.path.basename(file).split('.')[0]}.txt", val, ans)  # fmt: skip
            except NotADirectoryError:
                # if input is a file
                # print("Running " + ALGO_NAME[choice - 1] + " on " + input_path)
                val, ans, time, mem = unit(input_path, ALGO[choice - 1])
                if output_flag:
                    report_append(ALGO[choice - 1].__name__ + "," + os.path.basename(input_path), time, mem)
                    fo.write_file(f"test/output/{ALGO_NAME[choice - 1]}/OUTPUT_{os.path.basename(input_path).split('.')[0]}.txt", val, ans)  # fmt: skip

            print("Press [ENTER] to continue...")
            input()
            menu_handler()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if len(sys.argv) > 1:
        demo()
    else:
        menu_handler()
