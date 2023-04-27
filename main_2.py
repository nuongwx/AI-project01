import time
import psutil
import os
import brute_force as bf_old
import brutev2 as bf

# import branch_and_bound as br_old
import branchv2 as br

import beam as bm

import genetic_algorithms as ga

class RunAlgorithm:
    def case(self, filename):
        capacity = 0
        number_of_classes = 0
        weights = []
        values = []
        class_label = []

        # Open the file
        f = open(filename, "r")
        lines = f.readlines()
        capacity = int(lines[0])
        number_of_classes = int(lines[1])
        weights = [float(i) for i in lines[2].split(',')]
        values = [int(i) for i in lines[3].split(',')]
        class_label = [int(i) for i in lines[4].split(',')]
        f.close()
        return {
            "capacity": capacity,
            "number_of_classes": number_of_classes,
            "weights": weights,
            "values": values,
            "labels": class_label
        }

    def run(self):
        print("1. Brute Force")
        print("2. Branch and Bound")
        print("3. Local Beam Search")
        print("4. Genetic Algorithm")
        choice = int(input("Select an algorithm: "))
        testCase = input("Select a test case (choose from 1-10): ")
        use_case = self.case("test/input/INPUT_" + testCase + ".txt")
        fout = open("test/output/OUTPUT_" + testCase + ".txt", "w")
        # if choice == 1:
        #     BF = bf.BruteForce(use_case)
        #     result = BF.run()
        #     fout = open("test/output/brute_force/OUTPUT_" + testCase + ".txt", "w")
        #     fout.write(str(result[0]) + '\n')
        #     fout.write(str(result[1]))
        # elif choice == 2:
        #     BAB = br.run(use_case)

        # elif choice == 3:
        #     beamSearch = BeamSearch()
        #     beamSearch.run(ks, fout)
        if choice == 4:
            Gen = ga.GeneticAlgorithm(use_case)
            result = Gen.run()
            fout = open("test/output/genetic_algorithms/OUTPUT_" + testCase + ".txt", "w")
            fout.write(str(result[0]) + '\n')
            fout.write(str(result[1]))

process = psutil.Process(os.getpid())
start_time = time.time()
runAlgorithm = RunAlgorithm()
runAlgorithm.run()
print("Runtime: --- %s seconds ---" % (time.time() - start_time))
print("Memory: --- ", end="")
print(process.memory_info().rss / (1024 * 1024), end="")
print(" MB ---", end="")