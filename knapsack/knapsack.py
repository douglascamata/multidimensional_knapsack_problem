from time import clock
from copy import deepcopy


class Item(object):

    def __init__(self, name, value, weight, volume):
        self.name = name
        self.value = value
        self.weight = weight
        self.volume = volume

    def __repr__(self):
        return "<%s>" % self.name
        # return "<%s | %d >" % (self.name, self.value)

    def ratio(self):
        return float(self.value) / (self.weight + self.volume)

    def __eq__(self, item):
        return self.name == item.name and self.value == item.value and self.weight == item.weight and self.volume == item.volume
        

class Knapsack(object):

    def __init__(self, weight, volume, all_items, **kwargs):
        self.weight = self.initial_weight = weight
        self.volume = self.initial_volume = volume
        self.value = 0
        self.all_items = all_items
        self.initial_value = 0
        self.items = []
        self.movement_counter = 0
        self.moves_made = []
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def optimize(self, initial_solution_function, heuristic_function, neighborhood_function):
        start = clock()
        initial_solution_function(self)
        self.initial_solution = deepcopy(self.items)
        self.initial_value = self.value
        heuristic_function(neighborhood_function, self)
        end = clock()
        print 'Best solution found with %d move(s).' % len(self.moves_made)
        print 'Initial solution was: %s' % self.initial_solution
        print 'Movements made: '
        for move in self.moves_made:
            print '-'*3 + " %s " % str(move)
        print 'Initial value: %d' % self.initial_value
        print 'Final value: %d' % self.value
        print 'Total improvement: %d' % (self.value - self.initial_value)
        print 'Weight left: %d' % self.weight
        print 'Volume left: %d' % self.volume
        print 'Number of items in solution: %s' % len(self.items)
        print 'Ran in %f milliseconds.' % ((end-start)*1000)

    def execute_movement(self, movement, silent=False):
        for item in movement.remove_items:
            if not item in self:
                return False
            self.remove_item(item)
        for item in movement.add_items:
            if not self.can_add_item(item):
                return False
            self.add_item(item)
        if not silent:
            self.movement_counter += 1
            self.moves_made.append(movement)
        return True

    def add_item(self, item):
        if self.can_add_item(item):
            self.items.append(item)
            self.weight -= item.weight
            self.volume -= item.volume
            self.value += item.value
            self.all_items.remove(item)
            return True
        return False

    def evaluate_swap(self, item, another_item):
        return self.can_swap(item, another_item)

    def remove_item(self, item):
        if item in self.items:
            self.weight += item.weight
            self.volume += item.volume
            self.value -= item.value
            self.items.remove(item)
            self.all_items.append(item)
            return True
        return False

    def can_swap(self, inside_item, another_item):
        if not inside_item in self or another_item in self:
            return False
        new_weight = self.weight + inside_item.weight
        new_volume = self.volume + inside_item.volume
        if (another_item.weight <= new_weight and another_item.volume <= new_volume):
            return self.value - inside_item.value + another_item.value
        return False

    def swap(self, item, another_item):
        if self.can_swap(item, another_item):
            self.remove_item(item)
            self.add_item(another_item)
            return True
        return False

    def __contains__(self, item):
        return any(map(lambda x: x == item, self.items))

    def can_add_item(self, item):
        if (self.weight >= item.weight and self.volume >= item.volume and not item in self.items):
            return True
        return False

    def __repr__(self):
        return "<Knapsack (%d) %s>" % (len(self.items), repr(self.items))

    def sorted_items(self, items, key=Item.ratio):
        return sorted(items, key=key, reverse=True)

    def solution_neighborhood(self, f):
        return f(self)


class Movement(object):

    def __init__(self, add_items=[], remove_items=[]):
        self.add_items = add_items
        self.remove_items = remove_items

    @property
    def movement_avaliation(self):
        remove_value = add_value = 0
        if not len(self.remove_items) == 0:
            remove_value = reduce(lambda x, y: x + y, [item.value for item in self.remove_items])
        if not len(self.add_items) == 0:
            add_value = reduce(lambda x, y: x + y, [item.value for item in self.add_items])
        return add_value - remove_value

    def reverse(self):
        return Movement(add_items=self.remove_items, remove_items=self.add_items)

    def __eq__(self, another_move):
        if not isinstance(another_move, Movement):
            return False
        return self.add_items == another_move.add_items and self.remove_items == another_move.remove_items

    def __repr__(self):
        # return "<Improve %d>" %  self.movement_avaliation
        return "<Remove %s | Add %s | Improve %d>" % (self.remove_items, self.add_items, self.movement_avaliation)