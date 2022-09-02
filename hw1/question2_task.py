import gurobipy as gp
import numpy as np

# number of tasks
num_tasks = 8

# set of precedences
P = [[], [0], [0], [0, 2], [1, 2], [3], [1, 2, 5], [3, 4], [i for i in range(num_tasks)]]

# set of duration time
# s = np.random.randint(20, size=8)
s = [13, 11, 8, 14, 9, 3, 17, 14]
print("duration time", s)

# create model
m = gp.Model("task")
# create variables
x = m.addVars(num_tasks + 1, lb=0)
# add constraints
cons = m.addConstrs(x[i] >= x[j] + s[j] for i in range(num_tasks + 1) for j in P[i])
# set objective function
m.setObjective(x[num_tasks])

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
for i in range(num_tasks + 1):
    print("Start time of task", i, "is", x[i].x)