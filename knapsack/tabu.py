from copy import deepcopy

class TabuList(list):

    def __init__(self, size=3):
        self.size = size
        super(TabuList, self).__init__()

    def append(self, element):
        if len(self) == self.size:
            self.pop(0)
            return super(TabuList, self).append(element)
        return super(TabuList, self).append(element)

    def __contains__(self, move):
        for i in range(len(self)):
            if move == self[i]:
                return True
        return False


class TabuSearch(object):

    def __init__(self, max_iter=2):
        self.iter_counter = 0
        self.iter_better = 0
        self.max_iter = max_iter

    def __call__(self, neighborhood_function, knapsack):
        solutions = neighborhood_function(knapsack)
        sorted_moves = self.sort_moves(solutions)
        [sorted_moves.remove(tabu.reverse()) for tabu in knapsack.tabu_list if tabu.reverse() in sorted_moves]
        best_move = None
        best_solution = knapsack.value
        best_solution_moves = deepcopy(knapsack.moves_made)
        best_solution_items = deepcopy(knapsack.items)
        tabu_ended = False

        while self.iter_counter - self.iter_better < self.max_iter:
            self.iter_counter += 1
            if not len(sorted_moves) == 0: # se a lista tabu nao eliminou todos vizinhos
                candidate_move = sorted_moves.pop(0) # pegar o melhor movimento possivel
                actual_solution = knapsack.value + candidate_move.movement_avaliation
                knapsack.execute_movement(candidate_move)
                knapsack.tabu_list.append(candidate_move.reverse())
                if actual_solution > best_solution:
                    print "Current iter %d, actual solution %d, better solution found in %d with %d" % (self.iter_counter, actual_solution, self.iter_better, best_solution)
                    best_solution = actual_solution
                    best_solution_moves = deepcopy(knapsack.moves_made)
                    best_solution_items = deepcopy(knapsack.items)
                    self.iter_better = self.iter_counter
            else: # se eliminou todos vizinhos
                # encontra o tabu com melhor melhora
                # if len(knapsack.tabu_list) == 0:
                    # return False
                best_tabu = reduce(lambda x, y: x if x.movement_avaliation > y.movement_avaliation else y, knapsack.tabu_list)
                if best_tabu.movement_avaliation > 0: # se ele apresentar uma melhora real na solucao atual
                    actual_solution = knapsack.value + best_tabu.movement_avaliation
                    if actual_solution > best_solution:
                        print "[TABU] Current iter %d, actual solution %d, better solution found in %d with %d" % (self.iter_counter, actual_solution, self.iter_better, best_solution)
                        best_solution = actual_solution
                        best_solution_moves = deepcopy(knapsack.moves_made)
                        best_solution_items = deepcopy(knapsack.items)
                        self.iter_better = self.iter_counter
                    knapsack.execute_movement(best_tabu)
            solutions = neighborhood_function(knapsack)
            sorted_moves = self.sort_moves(solutions)
            [sorted_moves.remove(tabu.reverse()) for tabu in knapsack.tabu_list if tabu.reverse() in sorted_moves]
            # print "Current iter %d, actual solution %d, better solution found in %d with %d" % (self.iter_counter, actual_solution, self.iter_better, best_solution)

        print "Better solution found in %d with %d" % (self.iter_better, best_solution)
        print knapsack.value
        print best_solution
        knapsack.value = best_solution
        knapsack.items = best_solution_items
        knapsack.moves_made = best_solution_moves
        
        print 'Script ran with tabu search using a max of %d iterations and a tabu list with size %d.' % (self.max_iter, knapsack.tabu_list.size)
        if not tabu_ended:
            print 'Ended by iteration limit.'
        return False

    def sort_moves(self, moves):
        return sorted(moves, key=lambda x: x.movement_avaliation, reverse=True)

