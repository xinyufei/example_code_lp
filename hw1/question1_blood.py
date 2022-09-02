import gurobipy as gp
import numpy as np

# define parameters
# type of blood
num_blood = 4
blood_type = ['A', 'B', 'AB', 'O']
# number of locations
num_locations = 7
# supply set
S = {0, 1, 2, 3, 4, 5}
# demand set
D = {0, 1, 2, 4, 6}
# product capacity for each blood type
capacity = [[40, 0, 20, 70], [0, 40, 80, 0], [40, 0, 0, 0], [30, 10, 30, 30],
            [20, 80, 0, 30], [0, 0, 0, 50], [0, 0, 0, 0]]
# demand for each blood type
demand = [[0, 50, 0, 0], [70, 0, 0, 30], [0, 10, 60, 60], [0, 0, 0, 0], [0, 0, 30, 0], [0, 0, 0, 0], [10, 10, 10, 10]]
# cost for all the nodes
cost = [[1, 50, 10, 30, 20, 10, 20], [50, 1, 10, 30, 10, 10, 20], [10, 10, 1, 60, 30, 10, 20],
        [30, 30, 60, 1, 10, 10, 20], [20, 10, 30, 10, 1, 10, 20], [10, 10, 10, 10, 10, 1, 10],
        [10, 10, 10, 10, 10, 10, 1]]

# create a model
m = gp.Model("blood")
# create variables
x = m.addVars(num_locations, num_locations, num_blood, lb=0)
# add supply constraints
m.addConstrs(gp.quicksum(x[i, j, k] for j in D) <= capacity[i][k] for i in S for k in range(num_blood))
# add demand constraints
# constraint for type O
m.addConstrs(gp.quicksum(x[i, j, 3] for i in S) >= demand[j][3] for j in D)
# constraint for type A
m.addConstrs(gp.quicksum(x[i, j, 0] + x[i, j, 3] for i in S) >= demand[j][0] + demand[j][3] for j in D)
# constraint for type B
m.addConstrs(gp.quicksum(x[i, j, 1] + x[i, j, 3] for i in S) >= demand[j][1] + demand[j][3] for j in D)
# constraint for type AB
m.addConstrs(gp.quicksum(x[i, j, k] for i in S for k in range(num_blood)) >=
             gp.quicksum(demand[j][k] for k in range(num_blood)) for j in D)
# set objective value
m.setObjective(gp.quicksum(cost[i][j] * x[i, j, k] for i in S for j in D for k in range(num_blood)))

# optimize the model
m.optimize()

# print optimal value
print("The optimal value is", m.objval)

# print optimal solutions
for k in range(num_blood):
    for i in range(num_locations):
        for j in range(num_locations):
            if x[i, j, k].x > 0:
                print("non-zero unit of blood type", blood_type[k], "on arc", (i, j), "is", x[i, j, k].x)