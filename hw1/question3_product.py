import gurobipy as gp
import numpy as np

# number of time periods
num_time_periods = 8
# demand quantity
# d = np.random.randint(20, 40, size=num_time_periods)
# print("demand quantity", d)
d = [27, 32, 23, 22, 31, 20, 39, 38]
# cost for production
# c = np.random.uniform(20, size=num_time_periods)
# print("cost for production", c)
c = [1.51178505, 4.03937645, 10.24849733, 18.74598538, 7.12537098, 19.6879297, 8.01831219, 16.26632789]
# cost for stocks
# h = np.random.uniform(20, size=num_time_periods)
# print("cost for stocks", h)
h = [9.40129954, 11.26772831, 17.8973554, 3.085775, 13.89510398, 11.1470197, 3.99916813, 8.55679761]
# cost for backlogging
# b = np.random.uniform(20, size=num_time_periods)
# print("cost for backlogging", b)
b = [18.92339065, 17.21817062, 14.21969859, 1.27895396, 11.39852461, 5.74489424, 18.12854902, 18.48923752]

# create model
m = gp.Model("production")
# create variables
x = m.addVars(num_time_periods, lb=0)
s = m.addVars(num_time_periods, lb=0)
l = m.addVars(num_time_periods, lb=0)
# add constraints
m.addConstr(x[0] + l[1] == d[0] + s[0])
m.addConstrs(s[t - 1] + x[t] + l[t + 1] == d[t] + s[t] + l[t] for t in range(1, num_time_periods - 1))
m.addConstr(s[num_time_periods - 2] + x[num_time_periods - 1] == d[num_time_periods - 1] + l[num_time_periods - 1])
# set objective function
m.setObjective(gp.quicksum(c[t] * x[t] + h[t] * s[t] + b[t] * l[t] for t in range(num_time_periods)))

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
for t in range(num_time_periods):
    print("The units of production, stock, and backlogging of time period", t, "is", x[t].x, s[t].x, l[t].x)