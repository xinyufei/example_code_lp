#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 11:46:06 2022

@author: xinyuf
"""

# import gurobi-python to use it
import gurobipy as gp

# define parameters for the model
# number of plans (m in the slides) 
num_plants = 8
# an alternative definition:
plant = {0, 1, 2, 3, 4, 5, 6, 7}
# number of warehouse (n in the slides)
num_warehouse = 6
# an alternative definition:
warehouse = {0, 1, 2, 3, 4, 5}
# costs for each edge
# This is a two-dimensional list with size num_plants * num_warehouse
# For simplicity, we define all the costs as integer values. For your instance, 
# you can define any costs you like. 
cost = [[3, 1, 1, 2, 3, 1],
        [5, 2, 5, 2, 1, 5],
        [2, 2, 5, 3, 4, 2],
        [5, 4, 5, 5, 4, 5],
        [5, 2, 2, 2, 5, 3],
        [4, 5, 5, 5, 2, 1],
        [1, 1, 1, 5, 3, 5],
        [2, 3, 4, 1, 4, 4]]
# Production capacity (a in the slides). It is a vector with size num_plants
capacity = [3, 8, 5, 9, 9, 6, 13, 15]
# Demand (b in the slides). It is a vector with size num_warehouse
demand = [8, 13, 8, 6, 11, 9]

# define a new model with name diet
m = gp.Model("transportation")

# define new variables (x in the slides)
# The variables is defined as a matrix with size num_plants * num_warehouse
arcs = m.addVars(num_plants, num_warehouse, lb=0, ub=gp.GRB.INFINITY, name="arcs")

# Add demand constraints for each warehouse
# We get x_ij by arcs[i,j] in the variable
m.addConstrs((gp.quicksum(arcs[i, j] for i in range(num_plants)) >= demand[j] for j in range(num_warehouse)),
             name="demand")
# # an alternative formualtion
# m.addConstrs((gp.quicksum(arcs[i, j] for i in plant) >= demand[j] for j in warehouse), name="demand_alt")
# Add capacity constraints for each plant
m.addConstrs((gp.quicksum(arcs[i, j] for j in range(num_warehouse)) <= capacity[i] for i in range(num_plants)),
             name="capacity")
# # an alternative formualtion
# m.addConstrs((gp.quicksum(arcs[i, j] for j in warehouse) <= capacity[i] for i in plant), name="capacity_alt")
# Set objective function to minimize the total cost
m.setObjective(gp.quicksum(cost[i][j] * arcs[i, j] for i in range(num_plants) for j in range(num_warehouse)),
               gp.GRB.MINIMIZE)

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
for i in range(num_plants):
    for j in range(num_warehouse):
        if arcs[i, j].x > 0:
            print("non-zero unit on arc", (i, j), "is", arcs[i, j].x)
