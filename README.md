# MetaHeuristic
Project for the exam of "Logistic Optimization"

This application implements and compares the performance of the meta-heuristic techniques **Tabu Search** (TS) and **Variable Neighborhood Search** (VNS) for the ***Parallel Machine Scheduling Problem***. The main feature of these approaches is the provisioning of a lower bound for the optimal solution, individuating local optimal, acting as a *guarantee* of the goodness of the global optimal. The local optima could even be the best possible solution.

## Requirements and utilization:
The application is entirely written in Python (version 3.7). The only requirement is the module *PrettyTable* for tables handling.
> pip install PrettyTable

To test the implementations is enough to run the script *main.py* from the command line. At the completion, the user will see tables containing final results, which are also in the *logs* folder.

## The problem:
The *parallel machine scheduling problem* is the individuation of the best schedule on identical machines of tasks named *jobs*, aimed at minimizing:

> ![Objective function](https://user-images.githubusercontent.com/27780725/145707304-39278219-0d2d-4d99-80a4-29a2674927b2.png)

It is assumed that:
- All machines are available at time 0.
- The assigned jobs cannot stop (no preemption).
- Each machine can handle at most one job per time.
- The jobs allocated on the same machine follow Smith's rule, an increasing ordering based on the ratio weight/completion time. This condition ensures optimality on the single machine.

Both TS and VNS constitute research techniques of local minima, exploiting some tricks to get out of local minima to improve the discovered solutions. TNS and VNS contemplate the concept of "neighbourhood" in the space of the possible configurations, assuming that solutions in the same neighbourhood are in someway similar.

The looking for the minimum relies upon two different phases: **intensification** and **diversification**. The former looks for the best solution inside the given neighbourhood (i.e. Using gradient descent techniques), while the latter moves in the space to define new regions in which searching. The diversification can move in worse solutions zones to get out from convex zones that could block intensification techniques.

## Implementation:

### Starting Solutions
Both techniques need a feasible solution to improve during iterations. The choice of the initial configuration shouldn't impact the quality of the identified solution due to the previously mentioned diversification and intensification phases. The considered jobs randomly displace themselves on available machines, then ordered through Smith's rule. The allocation of the jobs on machines is named *schedule*, and it will be the starting point to reach the final solution.

### Definition of Neighbourhood
The current schedule allows choosing a **pivot element** using a random or deterministic approach. The permutation set appliable to the pivot defines the **neighbourhood**. Each permutation can belong to one of two categories:
- Swap (of the pivot with a job allocated on another machine).
- Spin (of a job on another machine).
Both these operations guarantee the validity of Smith's rule on each machine.

### Stopping criterion
Both approaches iterate up to a maximum number of steps or until a non-improving steps streak reaches a certain length. The user can define both these criteria.

### Solution Space Manager module (SSM.py)
The common characteristics between the two approaches coexist in a single module. Among the many methods, the most significant are essential to:
- Provide a starting and feasible solution.
- Compute the value of the objective function on the passed schedule.
- Update the completion time of the jobs on the machines after a permutation.

### Tabu Search (Tabu.py)
This technique shows a **Tabu List** containing the moves performed on the schedule, named **rules**. Each one is valid for a fixed number of iterations, corresponding to the square root of the number of jobs (N).
The diversification phase picks a random pivot to determine the next neighbourhood. Each neighbourhood adopts the best solution inside itself (intensification).

### Variable Neighbourhood Search (VNS.py)
The diversification phase, named **Shaking**, consists of the exploration of a random neighbourhood (random pivot), while the intensification phase explores all the structures associated with that neighbourhood (pivot = 0, ..., len_schedule - 1)

## Benchmark
The main script generates the initial fixed allocations of machines/jobs. Weights and completion time are random and superiorly limited by the parameter **Pmax**. The TS and VNS algorithms use identical instances. For each run, the algorithm writes a log containing the applied permutations. The main script produces two text files named results and data, containing respectively optimal values of the objective functions and corresponding configurations.

## Results
Setting the same iterations for both, TS is neatly faster than VNS but finds slightly worse solutions.
