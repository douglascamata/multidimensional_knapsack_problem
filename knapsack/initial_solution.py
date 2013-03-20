from copy import deepcopy
from random import shuffle

def random_add_solution(knapsack):
    all_items = deepcopy(knapsack.all_items)
    parar = False
    shuffle(all_items)
    for item in all_items:
        if knapsack.can_add_item(item):
            knapsack.add_item(item)
        else:
            continue


def greedy_solution(knapsack):
    items = knapsack.sorted_items(knapsack.all_items)
    [knapsack.add_item(item) for item in items]