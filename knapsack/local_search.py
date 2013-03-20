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
