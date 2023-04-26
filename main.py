import os, sys  # path manip, system calls
import timeit  # time measurements

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
    with open("stats.csv", "w+") as f:
        f.write("\n")
        os.mkdir(os.path.normpath(os.getcwd() + "/test/output"))
        for idx, i in enumerate(ALGO):
            print(f"Running {ALGO_NAME[idx]}")
            os.mkdir(os.path.normpath(os.getcwd() + f"/test/output/{ALGO_NAME[idx]}"))
            f.write(f"{ALGO_NAME[idx]}, ")
            for j in range(0, 10):
                print(f"Case {j + 1}")
                # ignore large cases for brute force
                if i == ALGO[0] and j > 4:
                    f.write("-1, ")
                    continue
                #
                case = fo.read_file(f"test/input/INPUT_{j + 1}.txt")
                start = timeit.default_timer()
                # mem1 = mem_profile.memory_usage()
                val, ans = i.run(case)
                # mem2 = mem_profile.memory_usage()
                stop = timeit.default_timer()
                fo.write_file(f"test/output/{ALGO_NAME[idx]}/OUTPUT_{j + 1}.txt", val, ans)
                # writer.writerow(["", stop - start, mem2[0] - mem1[0]])
                f.write(f"{stop - start}, ")
                f.flush()
                os.fsync(f.fileno())
            f.write("\n")


def unit(filename, algo):
    try:
        case = fo.read_file(f"{filename}")
    except FileNotFoundError or ValueError:
        print(filename + " is invalid")
        return -1, [], -1
    start = timeit.default_timer()
    val, ans = algo.run(case)
    stop = timeit.default_timer()
    print("Task completed in", stop - start, "seconds")
    return val, ans, stop - start


def error_message(message, fp):
    print(message)
    print("Press [ENTER] to continue or [CTRL + C] to exit")
    input()
    return fp()


def algorithms_menu():
    print("\033[H\033[J")
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
    print("\033[H\033[J")
    print("INPUT")
    print("1. Input from txt file")
    print("2. Input from folder")
    print("0. Back")
    print("Current working directory: " + os.getcwd())
    print("Enter your choice or press [ENTER] to run defaults: ", end="")
    try:
        text = input()
        if text == "":
            return path_clean_and_check("test/input")
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
            val, ans, time = 0, 0, []
            # creating output necessities
            output_flag = boolean_input("Do you want to save output and stats?")
            if output_flag:
                print("Saving to test/output and stats.csv")
                if not os.path.exists("test/output"):
                    os.mkdir("test/output")
                if not os.path.exists("test/output/" + ALGO_NAME[choice - 1]):
                    os.mkdir("test/output/" + ALGO_NAME[choice - 1])
                if os.path.exists("stats.csv"):
                    if boolean_input("stats.csv already exists. Do you want to overwrite?"):
                        os.remove("stats.csv")
            try:
                # if input is a folder
                file_list = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
                for file in file_list:
                    print(f"Running {ALGO_NAME[choice - 1]} on {file}")
                    val, ans, temp_time = unit(f"{input_path}/{file}", ALGO[choice - 1])
                    time.append(temp_time)
                    if output_flag:
                        fo.write_file(f"test/output/{ALGO_NAME[choice - 1]}/OUTPUT_{os.path.basename(file).split('.')[0]}.txt", val, ans)  # fmt: skip
            except NotADirectoryError:
                # if input is a file
                print("Running " + ALGO_NAME[choice - 1] + " on " + input_path)
                val, ans, time = unit(input_path, ALGO[choice - 1])
                time = [time]
                if output_flag:
                    fo.write_file(f"test/output/{ALGO_NAME[choice - 1]}/OUTPUT_{os.path.basename(input_path).split('.')[0]}.txt", val, ans)  # fmt: skip
            # write stats
            if output_flag:
                with open("stats.csv", "w+") as f:
                    f.write(f"{ALGO_NAME[choice - 1]}" + ", ".join([str(i) for i in time]) + "\n")

            print("Press [ENTER] to continue...")
            input()
            menu_handler()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if len(sys.argv) > 1:
        demo()
    else:
        menu_handler()
