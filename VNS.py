from SSM import *

"""
Implementation of metaheuristic "Variable Neighborhood Search"

This metaheuristic has a very similar approach to Tabu Search.
    - They have an exploration of a local neighborhood of the current solution
    - They choose one element of the local neighborhood and reiterate until a stop condition (step number, consecutive non-ameliorative steps, ...)
"""

"""
Execute variable neighborhood search implementation using methods provided by SSM module
"""
def run(machines, jobs, maxSimulationSteps, maxNonImprovingSteps):
    simulationStep = 0
    nonImprovingSteps = 0

    file = open("logs/vns/" + str(len(jobs)) + "J_" + str(len(machines)) + "M.txt", "w+", newline='\n')

    schedule, bestValue = setup(machines, jobs, file)
    bestSchedule = schedule.copy()
    file.write("\nStarting iterations... \n")

    while simulationStep < maxSimulationSteps:
        simulationStep += 1
        file.write("\n### Iteration " + str(simulationStep) + " ###\n")
        pivot = 0
        while pivot < len(schedule):
            candidates, pivotIndex = getNeighbor(machines, schedule, file, pivot)
            file.write("\nSelected Neighborhood: " + str(candidates) + "\n")
            # Variable Neighborhood Search selects a random solution of the given neighborhood
            getMin(candidates, schedule, pivotIndex, file, False)
            file.write("\nRandomly chosen solution: " + str(schedule) + "\n")

            # Local Search is exploited on randomly selected solution to retrieve the better solution on its neighborhood
            candidates, pivotIndex = getNeighbor(machines, schedule, file, pivot)
            file.write("\nCandidates of iteration " + str(simulationStep) + "\n")
            move, minValue = getMin(candidates, schedule, pivotIndex, file, True)
            updateSchedule(schedule, machines)

            if minValue < bestValue:
                file.write("New minimum found (" + str(minValue) + "), storing...\n")
                nonImprovingSteps = 0
                bestValue = minValue
                bestSchedule = schedule.copy()
            else:
                nonImprovingSteps += 1
                if nonImprovingSteps >= maxNonImprovingSteps:
                    file.write("Maximum non improving steps reached, quitting...\n")
                    break

            pivot += 1

        if nonImprovingSteps >= maxNonImprovingSteps:
            break
        file.write(str(nonImprovingSteps) + " non improving steps\n")

    file.write("\n###\n" + str(simulationStep) + " steps done, best schedule is \n" + str(bestSchedule) + "\nvalue " + str(bestValue) + "\n###\n")
    file.close()
    return bestValue, bestSchedule
