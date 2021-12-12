from random import randint
import Tabu
import VNS
from time import process_time
from prettytable import PrettyTable

"""
This script generates machines and jobs for testing the implemented metaheuristics
"""

def allocateJobs(j, pMax):
    jobs = []
    for i in range(j):
        # Job's name, weight and time
        weight = randint(1, pMax)
        time = randint(1, pMax)
        jobs.append(["J"+str(i), weight, time, round(weight/time, 2)])
    return jobs

def allocateMachines(m):
    machines = []
    for i in range(m):
        machines.append("M"+str(i))
    return machines

def printValues(values, title, results, data):
    t = PrettyTable()
    t.field_names = ['Jobs Number', 'Machines Number', 'Value', 'Time (s)']
    for v in values:
        t.add_row([v[0], v[1], v[2][0], v[3]])
        data.write(title + "\n")
        data.write(str(v[0]) + " jobs, " + str(v[1]) + " machines\n")
        data.write("Value: " + str(v[2][0]) + "\n")
        data.write(str(v[2][1]) + "\n\n")
    print(t)
    results.write(title + "\n")
    results.write(str(t) + "\n\n\n")

def compareResults(heuristic1, heuristic2, first_column, second_column, title, results):
    t = PrettyTable()
    t.field_names = ["Jobs Number", "Machines Number", first_column, second_column, "Ratio"]
    # heuristic1 and heuristic2 have the same length
    for i in range(len(heuristic1)):
        ratio = heuristic2[i][2][0] / heuristic1[i][2][0]
        t.add_row([heuristic1[i][0], heuristic1[i][1], heuristic1[i][2][0], heuristic2[i][2][0], round(ratio, 5)])
    print(t)
    results.write(title + "\n")
    results.write(str(t) + "\n\n\n")


if __name__ == "__main__":

    # Distribution adopted for generating jobs and machines
    jobsNumber = [30, 100, 400]
    machinesNumber = [2, 4, 6, 8, 16, 30]
    pMax = 20

    jobs = []
    machines = []

    bestTabuResults = []
    bestVNSResults = []

    maxSimulationSteps = 0
    maxNonImprovingSteps = 0

    results = open("results.txt", "w+", newline='\n')
    data = open("data.txt", "w+", newline='\n')

    while True:
        try:
            maxSimulationSteps = int(input("Insert simulation steps: "))
            maxNonImprovingSteps = int(input("Insert maximum non improving steps: "))
        except:
            print("Error in input, retry...")
            continue
        break

    for j in jobsNumber:

        jobs = allocateJobs(j, pMax)

        for m in machinesNumber:
            if m < j/2:
                machines = allocateMachines(m)

                print("Testing " + str(j) + " jobs on " + str(m) + " machines (Tabu Search)")
                start = process_time()
                bestTabuResults.append([j, m, Tabu.run(machines, jobs, maxSimulationSteps, maxNonImprovingSteps), round(process_time() - start, 5)])

                print("Testing " + str(j) + " jobs on " + str(m) + " machines (Variable Neighborhood Search)")
                start = process_time()
                bestVNSResults.append([j, m, VNS.run(machines, jobs, maxSimulationSteps, maxNonImprovingSteps), round(process_time() - start, 5)])
            else:
                break

    print("\n### Done ###\n")

    print("\n\nPrinting Tabu (TS) results")
    printValues(bestTabuResults, "TS", results, data)

    print("\n\nPrinting Variable Neighborhood Search (VNS) results")
    printValues(bestVNSResults, "VNS", results, data)

    print("\n\nComparison between TS and VNS")
    compareResults(bestTabuResults, bestVNSResults, "TS Values", "VNS Values", "Performance comparison between Tabu and VNS", results)
