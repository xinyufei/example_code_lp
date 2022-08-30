#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 11:46:06 2022

@author: xinyuf
"""

# import gurobi-python to use it
import gurobipy as gp 
# import numpy to randomly generate data for created instances
import numpy as np

# define parameters for the model
# number of plans (m in the slides) 
num_plants = 8
# number of warehouse (n in the slides)
num_warehouse = 6
# costs for each edge
# This is a two-dimensional list with size num_plants * num_warehouse
# For simplicity, we assume that the cost of each edge is generated from 
# {1, 2, 3, 4, 5} with equal probability.    
cost = np.random.randint(1, 5, size=(num_plants, num_warehouse))
print("The cost matrix is \n", cost)
# Production capacity (a in the slides). It is a vector with size num_plants
# For simplicity, we assume that the product capacity of each plant is generated from 
# {5, 6, ..., 15} with equal probability. 
capacity = np.random.randint(5, 15, size=num_plants)
print("The capacity of all the plants is", capacity)
# Demand (b in the slides). It is a vector with size num_warehouse
# For simplicity, we assume that the demand of each warehouse is generated from 
# {5, 6, ..., 15} with equal probability. 
demand = np.random.randint(5, 15, size=num_warehouse)
print("The demand of all the warehouses is", demand)

# define a new model with name diet
m = gp.Model("transportation")

# define new variables (x in the slides)
# The variables is defined as a matrix with size num_plants * num_warehouse
arcs = m.addVars(num_plants, num_warehouse, lb=0, ub=gp.GRB.INFINITY, name="arcs")

# Add demand constraints for each warehouse
# We get x_ij by arcs[i,j] in the variable
m.addConstrs((gp.quicksum(arcs[i, j] for i in range(num_plants)) >= demand[j] for j in range(num_warehouse)), name="demand")
# Add capacity constraints for each plant
m.addConstrs((gp.quicksum(arcs[i, j] for j in range(num_warehouse)) <= capacity[i] for i in range(num_plants)), name="capacity")

# Set objective function to minimize the total cost
m.setObjective(gp.quicksum(cost[i][j] * arcs[i, j] for i in range(num_plants) for j in range(num_warehouse)), gp.GRB.MINIMIZE)

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
for i in range(num_plants):
    for j in range(num_warehouse):
        if arcs[i, j].x > 0:
            print("non-zero unit on arc", (i, j), "is", arcs[i, j].x)

