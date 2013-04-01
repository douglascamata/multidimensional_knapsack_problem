import sys
from copy import deepcopy
from knapsack import *

def items_from_file(filename):
    items = []
    lines = open(filename).readlines()
    lines = [line.strip().split(' ') for line in lines]
    numbers_of_items = int(lines[0][1])
    for i in range(numbers_of_items):
        item = Item("Item %d" % i, int(lines[1][i]), int(lines[3][i]), int(lines[4][i]))
        items.append(item)
    return items

def bag_constraints_from_file(filename):
    items = []
    lines = open(filename).readlines()
    lines = [line.strip().split(' ') for line in lines]
    return int(lines[2][0]), int(lines[2][1])

def bag_from_file(filename):
    constraints = bag_constraints_from_file(filename)
    return (constraints[0], constraints[1], items_from_file(filename))

if __name__ == '__main__':
    # items = [
    #             Item(name, value, weight, volume) for name, value, weight, volume in \
    #             [
    #                 ('Apple', 2, 1, 2), ('Laptop', 3, 2, 1), ('Pen', 3, 1, 3),
    #                 ('Cap', 4, 3, 2), ('Cookie', 4, 2, 2), ('iPod', 5, 3, 3)
    #             ]
    #         ]

    bag = Knapsack(*bag_from_file('data.txt'), tabu_list=TabuList(200))
    bag.optimize(random_add_solution, TabuSearch(300), all_neighborhood)
    # bag.optimize(random_add_solution, first_improving_neighborhood, first_improving)
