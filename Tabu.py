from SSM import *
from math import sqrt

"""
Implementation of Tabu Search metaheuristic
"""


"""
Check if the couple (pivot, swapped) is in the tabu list or not.
It's important to remember that tabu moves are stored as (pivot element, swapped element) of the previous iteration, so is the opposite move 
(swapped element, pivot element) that cannot be applied, because it would mean going back.

Returns True if the passed move is forbidden, False otherwise
"""
def isTabu(pivot, swapped, tabuList, file):
    for t in tabuList:
        if t[0] == "Swap":
            if (t[2] == pivot and t[1] == swapped) or (t[2] == swapped and t[1] == pivot):
                file.write("Swap (" + str(pivot) + ", " + str(swapped) + ") is forbidden by tabu list " + str(tabuList) + "\n")
                return True
        else:   # "Spin"
            if t[1] == pivot and t[2] == swapped:
                file.write("Spin (" + str(pivot) + ", " + str(swapped) + ") is forbidden by tabu list " + str(tabuList) + "\n")
                return True
    return False


"""
Update tabu list's rules, adding the passed rule to it and decreasing pre-existent rules's duration and removing them if expired.
"""
def updateTabuList(tabuList, rule):
    # Before adding new move to tabu list, the old rules's Time To Live are decreased to remove the ones that are expired
    for t in range(len(tabuList)):
        tabuList[t][3] -= 1

    tabuList[:] = [t for t in tabuList if t[3] > 0]
    tabuList.append(rule)


"""
Execute tabu search implementation using methods provided by SSM module
"""
def run(machines, jobs, maxSimulationSteps, maxNonImprovingSteps):
    simulationStep = 0
    nonImprovingSteps = 0

    tabuList = []

    file = open("logs/tabu/" + str(len(jobs)) + "J_" + str(len(machines)) + "M.txt", "w+", newline='\n')

    schedule, bestValue = setup(machines, jobs, file)
    bestSchedule = schedule.copy()
    file.write("\nStarting iterations... \n")

    while simulationStep < maxSimulationSteps:

        simulationStep += 1
        file.write("\n### Iteration " + str(simulationStep) + " ###\n")

        candidates, pivotIndex = getNeighbor(machines, schedule, file)
        # candidates array is filtered to remove moves considered tabu
        candidates[:] = [c for c in candidates if not isTabu(c[1], c[2], tabuList, file)]
        file.write("\nCandidates of iteration " + str(simulationStep) + "\n")

        move, minVal = getMin(candidates, schedule, pivotIndex, file, True, int(sqrt(len(jobs))))
        updateSchedule(schedule, machines)

        """
        Tabu list stores move type, pivot element, second element of the move (other job or new machine) and TTL of the move in the tabu list
        Time To Live of the move is equal to square root of jobs's number
        """
        updateTabuList(tabuList, move)
        file.write("Current Tabu List: " + str(tabuList) + "\n")

        if minVal < bestValue:
            file.write("New minimum found (" + str(minVal) + "), storing...\n")
            nonImprovingSteps = 0
            bestValue = minVal
            bestSchedule = schedule.copy()
        else:
            nonImprovingSteps += 1
            if nonImprovingSteps >= maxNonImprovingSteps:
                file.write("Maximum non improving steps reached, quitting...\n")
                break

        file.write(str(nonImprovingSteps) + " non improving steps\n")

    file.write("\n###\n" + str(simulationStep) + " steps done, best schedule is \n" + str(bestSchedule) + "\nvalue " + str(bestValue) + "\n###\n")
    file.close()
    return bestValue, bestSchedule
