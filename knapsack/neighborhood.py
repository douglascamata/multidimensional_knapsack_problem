from knapsack import Movement
from random import choice, shuffle
from copy import deepcopy

def add_and_or_remove_neighborhood(knapsack):
    neighborhood = []
    improving = []
    shuffle(knapsack.items)
    for item in knapsack.items:
        if knapsack.can_add_item(item):
            movement = Movement(add_items=[item,])
            neighborhood.append(movement)
        else:
            weight_to_lose = item.weight
            volume_to_lose = item.volume
            items = deepcopy(knapsack.items)
            to_remove = choice(items)
            items.remove(to_remove)
            while not knapsack.can_swap(to_remove, item):
                print to_remove
                print item
                print '-'*80
                if len(items) == 0:
                    break
                to_remove = choice(items)
                items.remove(to_remove)
            else:
                movement = Movement(add_items=[item,], remove_items=[to_remove,])
                neighborhood.append(movement)
            print neighborhood
    return neighborhood


def all_neighborhood(knapsack):
    neighborhood = []
    improving_solutions = []
    shuffle(knapsack.all_items)
    for item in knapsack.all_items:
        i = 0
        actual_value = knapsack.value
        shuffle(knapsack.items)

        to_remove = []
        volume_to_lose = item.volume
        weight_to_lose = item.weight
        while volume_to_lose > 0 and weight_to_lose > 0:
            solution_item = choice(knapsack.items)
            to_remove.append(solution_item)
            weight_to_lose -= solution_item.weight
            volume_to_lose -= solution_item.volume
            i += 1
            movement = Movement(add_items=[item,], remove_items=to_remove)
            neighborhood.append(movement)

        for solution_item in knapsack.items:
            if knapsack.can_add_item(item):
                movement = Movement(add_items=[item,])
                neighborhood.append(movement)
            elif knapsack.can_swap(solution_item, item):
                new_value = knapsack.evaluate_swap(solution_item, item)
                movement = Movement(add_items=[item,], remove_items=[solution_item,])
                neighborhood.append(movement)
            else:
                continue
    return neighborhood

def first_improving_neighborhood(knapsack):
    neighborhood = []
    improving_solution = None
    for item in knapsack.sorted_items(knapsack.all_items):
        actual_value = knapsack.value
        for solution_item in knapsack.sorted_items(knapsack.items):
            if knapsack.can_swap(solution_item, item):
                new_value = knapsack.evaluate_swap(solution_item, item)
                movement = Movement(add_items=[item,], remove_items=[solution_item,])
                if new_value > knapsack.value:
                    improving_solution = movement
                    neighborhood.append(movement)
                    return neighborhood
                neighborhood.append(movement)
            else:
                pass
    return neighborhood