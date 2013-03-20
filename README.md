Multidimensional Knapsack Problem
=================================

A repository made to host something like a tiny framework to apply heuristics and metaheuristics to the 
multidimensional knapsack problem for a college exercise.

Instructions
------------

The **Knapsack** object receives in its constructor the two constraints for the problem (yes, it's still 
limited to two dimensions, but I'm working on this) and a array of **Items** that may be added to the
knapsack. Each **Item** have a **value** and how much of each constraint it consumes. Each additional
keyword argument will be converted into an attribute. This will provide some object injection
to implement some cool stuff.

To solve the problem, you use the method *optimize* and pass, in this order: the **initial solution
function** (that will receive the knapsack as its only parameter), **the local search function** (that
will receive the neighborhood function and the knapsack as parameters) and, the last but not least
important, the **neighborhood function**. 

**Note that it's the local search function responsibility to update
the execute movements in the knapsack's actual solution until some criteria is achieved.**

So, to clarify: `Knapsack.optimize(initial_solution_function, local_search_function, neighborhood_function)`

You may use the **Movement** class to create movements for the problem. It receives two arrays as arguments.
The first represents the Items that will be added to the solution and the second (guess what?) the **Items**
that will be removed from the **Knapsack**. The movement avaliation **(how it will affect the solution total value)**
is accessible through the `Movement.movement_avaliation` property. You can execute Movements by using the 
`Knapsack.execute_movement(movement)` method.

**For more useful methods on the Knapsack, like check if an Item can be added or removed from the Knapsack,
or if two Items, one out of the Knapsack and on inside it, can be swapped, check `knapsack/knapsack.py`.**

**You can find examples of initial solution functions, local search functions and neighborhood_functions
inside the knapsack folder in the respective files. Note that there's a file with a Tabu Search metaheuristic
implementation, which is the focus of this exercise.**
