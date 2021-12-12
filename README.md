# MetaHeuristic
Project for the exam of "Logistic Optimization"

This application implements and compares the performance of the meta-heuristic techniques **Tabu Search** (TS) and **Variable Neighborhood Search** (VNS) for the ***Parallel Machine Scheduling Problem***. The main feature of these approaches is the provisioning of a lower bound for the optimal solution, individuating local optimal, acting as a *guarantee* of the goodness of the global optimal. The local optima could even be the best possible solution.

The problem:
The *parallel machine scheduling problem* is the individuation of the best schedule on identical machines of tasks named *jobs*, aimed at minimizing:

> ![Objective function](https://user-images.githubusercontent.com/27780725/145707304-39278219-0d2d-4d99-80a4-29a2674927b2.png)

It is assumed that:
- All machines are available at time 0.
- The assigned jobs cannot stop (no preemption).
- Each machine can handle at most one job per time.
- The jobs allocated on the same machine follow Smith's rule, an increasing ordering based on the ratio weight/completion time. This condition ensures optimality on the single machine.

Both TS and VNS constitute research techniques of local minima, exploiting some tricks to get out of local minima to improve the discovered solutions. TNS and VNS contemplate the concept of "neighbourhood" in the space of the possible configurations, assuming that solutions in the same neighbourhood are in someway similar.

The looking for the minimum relies upon two different phases: **intensification** and **diversification**. The former looks for the best solution inside the given neighbourhood (i.e. Using gradient descent techniques), while the latter moves in the space to define new regions in which searching. The diversification can move in worse solutions zones to get out from convex zones that could block intensification techniques.
