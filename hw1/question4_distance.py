import gurobipy as gp
import numpy as np

# number of customers
num_customers = 12
# locations of customers
# location_x = np.random.uniform(-10, 10, num_customers)
# location_y = np.random.uniform(-10, 10, num_customers)
# print("locations of customers", location_x, location_y)
location_x = [-1.8984578, -3.26311439, 0.18379055, 1.76079939, 5.74823262, 1.22968313,
              0.23832401, 5.74869904, -5.64634626, 9.1869555, 0.48316226, -3.22117732]
location_y = [-0.95417693, 9.37962711, 2.55946717, 5.79327037, 3.70120793, 1.59074053,
              5.54955064, 1.6767642, -1.24780817, -8.45796729, -1.95505691, -3.07812864]

# create model
m = gp.Model("distance")
# create variables
u = m.addVars(num_customers, lb=0)
v = m.addVars(num_customers, lb=0)
a = m.addVar(lb=-gp.GRB.INFINITY)
b = m.addVar(lb=-gp.GRB.INFINITY)
# add constraints
m.addConstrs(location_x[i] - a <= u[i] for i in range(num_customers))
m.addConstrs(location_x[i] - a >= -u[i] for i in range(num_customers))
m.addConstrs(location_y[i] - b <= -v[i] for i in range(num_customers))
m.addConstrs(location_y[i] - b >= -v[i] for i in range(num_customers))
# set objective function
m.setObjective(gp.quicksum(u[i] + v[i] for i in range(num_customers)))

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
print("The location of library is", (a.x, b.x))