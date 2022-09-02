import gurobipy as gp

import numpy as np

# number of customers
num_customers = 15
# locations of customers
location_x = np.random.uniform(-10, 10, num_customers)
location_y = np.random.uniform(-10, 10, num_customers)
print("locations of customers", location_x, location_y)
# upper bound of distance
D = 8

# create model
m = gp.Model("distance")
# create variables
u = m.addVars(num_customers, lb=0)
v = m.addVars(num_customers, lb=0)
w = m.addVars(num_customers, lb=0)
z = m.addVars(num_customers, lb=0)
a = m.addVar(lb=-gp.GRB.INFINITY)
b = m.addVar(lb=-gp.GRB.INFINITY)
c = m.addVar(lb=-gp.GRB.INFINITY)
d = m.addVar(lb=-gp.GRB.INFINITY)
# add constraints
m.addConstrs(location_x[i] - a <= u[i] for i in range(num_customers))
m.addConstrs(location_x[i] - a >= -u[i] for i in range(num_customers))
m.addConstrs(location_y[i] - b <= -v[i] for i in range(num_customers))
m.addConstrs(location_y[i] - b >= -v[i] for i in range(num_customers))
m.addConstrs(location_x[i] - c <= w[i] for i in range(num_customers))
m.addConstrs(location_x[i] - c >= -w[i] for i in range(num_customers))
m.addConstrs(location_y[i] - d <= -z[i] for i in range(num_customers))
m.addConstrs(location_y[i] - d >= -z[i] for i in range(num_customers))
m.addConstr(a - c + b - d <= D)
m.addConstr(a - c + d - b <= D)
m.addConstr(c - a + b - d <= D)
m.addConstr(c - a + d - b <= D)
# set objective function
m.setObjective(gp.quicksum(u[i] + v[i] + w[i] + z[i] for i in range(num_customers)))

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
print("The location of library is", (a.x, b.x))
print("The location of mall is", (c.x, d.x))