from random import randint
from operator import itemgetter
from prettytable import PrettyTable

"""
Solution Space Manager, used to handle common operations between Tabu Search and Variable Neighborhood Search
"""

"""
Randomly allocate jobs to available machines to have an initial feasible solution
"""
def initAllocation(machines, jobs):
    schedule = []
    for j in jobs:
        schedule.append([machines[randint(0, len(machines)-1)], j[0], j[1], j[2], j[3], 0])

    return schedule


"""
This method evaluate the objective function applied on passed schedule

Schedule is defined as:
[Machine, job name, job weight, job required time, job ratio (weight/required time), job completion time on Machine], ...  
"""
def scheduleEvaluation(schedule, file):
    value = 0
    for s in schedule:
        value += float(s[2]) * s[5]

    file.write("Value: " + str(round(value, 2)) + "\n")
    return round(value, 2)


"""
After a schedule is changed, this function is in charge of update completion times
"""
def updateSchedule(schedule, machines):
    endTimes = {m: 0 for m in machines}
    for m in machines:
        endTimes[m] = 0

    for s in schedule:
        endTimes[s[0]] = endTimes[s[0]] + int(s[3])
        s[5] = endTimes[s[0]]


"""
Application of Smith Sorting on passed schedule, ordered using weight/time ratio
"""
def smithSorting(schedule):
    schedule.sort(key=itemgetter(4), reverse=True)


"""
Select an element of the schedule as pivot, evaluates solutions in the neighborhood gained through permutations
Return a list containing solutions in considered neighborhood and the index of used pivot
"""
def getNeighbor(machines, schedule, file, pivotIndex = -1):

    # pivot can be randomized (tabu search) or selected specifically (to produce a specific neighborhood)
    if pivotIndex == -1:
        pivotIndex = randint(0, len(schedule) - 1)

    pivot = schedule[pivotIndex]

    # candidates array stores solution of the considered neighborhood
    candidates = []

    """
    Job Swap in schedule
    """
    for s in schedule:

        # for each permutation of pivot with other jobs, evaluate schedule's value if machines differ
        if s[1] != pivot[1] and s[0] != pivot[0]:
            file.write("\nEvaluating swap of " + str(pivot[1]) + " and " + str(s[1]) + "\n")

            swapIndex = schedule.index(s)
            schedule[pivotIndex][0], schedule[swapIndex][0] = schedule[swapIndex][0], schedule[pivotIndex][0]
            updateSchedule(schedule, machines)

            # candidates list stores permutation type, pivot element, swapped element and value of objective function for that schedule
            candidates.append(['Swap', schedule[pivotIndex][1], schedule[swapIndex][1], scheduleEvaluation(schedule, file)])

            #  After swap, changes are reverted to return to original schedule
            schedule[swapIndex][0], schedule[pivotIndex][0] = schedule[pivotIndex][0], schedule[swapIndex][0]

    """
    Allocation of pivot on different machines
    """
    for m in machines:
        if m != pivot[0]:
            file.write("\nEvaluating allocation of job " + str(pivot[1]) + " (" + str(pivot[0]) + ") on machine " + m + "\n")
            oldMachine = schedule[pivotIndex][0]
            schedule[pivotIndex][0] = m
            updateSchedule(schedule, machines)

            candidates.append(['Spin', schedule[pivotIndex][1], m, scheduleEvaluation(schedule, file)])

            # Reverse of changes to come back to starting schedule
            schedule[pivotIndex][0] = oldMachine

    file.write("\nPivot: " + str(schedule[pivotIndex]) + "\n")

    return candidates, pivotIndex


"""
Handle initial allocation, ordering and first computation of completion times
Return starting schedule and associated value wrt objective function
"""
def setup(machines, jobs, file):
    schedule = initAllocation(machines, jobs)
    file.write("\nInitial allocation completed\n")

    # Smith's ordering is applied to the schedule, considering the weight/time ratio
    smithSorting(schedule)
    file.write("Schedule ordered\n")
    updateSchedule(schedule, machines)

    return schedule, scheduleEvaluation(schedule, file)


"""
Given admittable solutions gained from neighborhood, choose the next solution
Parameter getBetter leads this function towards the choosing of the solution with minimum value or towards a random one
Parameter TTL can be set for Tabu Search's rules, or let to default value (-1) in case of Variable Neighborhood Search
Return the move that transforms given schedule in the chosen one, and corresponding value wrt objective function
"""
def getMin(candidates, schedule, pivotIndex, file, getBetter, ruleTTL = -1):

    minVal = -1
    t = PrettyTable()
    t.field_names = ["Type of move", "Move", "Value"]
    for c in candidates:
        t.add_row([c[0], str(c[1])+"-"+str(c[2]), c[3]])

        if getBetter:
            if c[3] < minVal or minVal == -1:
                # minimum value between candidates swaps is always stored
                minVal = int(c[3])

    file.write(str(t) + "\n\n\n")

    if getBetter:
        # this function returns the index, in 'candidates' array, of the move corresponding to the best move found
        bestMove = [ind for ind in range(len(candidates)) if candidates[ind][3] == minVal].pop()
        file.write("\nBest move: ")
    else:
        # move to apply can even be chosen randomly (getBetter = False)
        bestMove = randint(0, len(candidates)-1)
        minVal = candidates[bestMove][3]
        file.write("\n(Randomly) selected move: ")

    file.write(str(candidates[bestMove]) + "\n")

    """
    Move selected is applied to current schedule
    """
    if candidates[bestMove][0] == 'Swap':
        pivotCoord = [ind for ind in range(len(schedule)) if candidates[bestMove][1] == schedule[ind][1]].pop()
        swapCoord = [ind for ind in range(len(schedule)) if candidates[bestMove][2] == schedule[ind][1]].pop()
        schedule[swapCoord][0], schedule[pivotCoord][0] = schedule[pivotCoord][0], schedule[swapCoord][0]
        move = [candidates[bestMove][0], schedule[pivotIndex][1], candidates[bestMove][2]]
    else:
        move = [candidates[bestMove][0], schedule[pivotIndex][1], schedule[pivotIndex][0]]
        schedule[pivotIndex][0] = candidates[bestMove][2]
    if ruleTTL != -1:
        # if ruleTTL is set (tabu search), it is added to chosen move
        move.append(ruleTTL)

    return move, minVal
