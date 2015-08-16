# Both local search functions in this file would need to be updated to actually
# execute movements in the knapsack and find a better solution. See the Tabu
# Search implementation for an idea of how to do this.
#
def best_improving(solutions, knapsack):
    sorted_solutions = sorted(solutions, key=lambda move: move.movement_avaliation, reverse=True)
    if len(sorted_solutions) == 0:
        return False
    if any(map(lambda solution: solution.movement_avaliation > 0, sorted_solutions)):
        return sorted_solutions[0]
    return False

def first_improving(solutions, knapsack):
    for solution in solutions:
        if solution.movement_avaliation > 0:
            return solution
    return False
