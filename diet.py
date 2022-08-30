#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 22:19:55 2022

@author: xinyuf
"""

# import gurobi-python to use it
import gurobipy as gp

# define parameters for the model
# number of different foods
num_food = 5
# name of foods
food_name = ["Chocolate", "Special K", "Steak", "Orange Juice", "Pizza"]
# price of foods
price = [0.75, 0.05, 1.5, 0.45, 1.25]
# fat of foods
fat = [5, 1, 1, 0, 10]
# Maximum bound on fat content
max_fat = 30
# calories of foods
cal = [250, 90, 300, 75, 400]
# Maximum bound on calories
max_cal = 2400
# protein of foods
protein = [1, 2, 3, 4, 5]
# Minimum requirement on protein
min_protein = 10

# define a new model with name diet
m = gp.Model("diet")

# define new variables (x in the slides)
# You can set lower bound and upperbound by giving values to lb and ub. 
# The default value is lb=0, ub=infinity
food = m.addVars(num_food, lb=0, ub=gp.GRB.INFINITY, name="food")

# add maximum constraint for fat
m.addConstr(gp.quicksum(fat[i] * food[i] for i in range(num_food)) <= max_fat, name="fat")
# Add maximum constraint for calories
m.addConstr(gp.quicksum(cal[i] * food[i] for i in range(num_food)) <= max_cal, name="calories")
# Add minimum constraint for protein
m.addConstr(gp.quicksum(protein[i] * food[i] for i in range(num_food)) >= min_protein, name="protein")

# Set objective function
# You can choose set it as minimization or maximization by setting gp.GRB.MINIMIZE or 
# gp.GRB.MAXIMIZE
m.setObjective(gp.quicksum(price[i] * food[i] for i in range(num_food)), gp.GRB.MINIMIZE)

# Optimize the model
m.optimize()

# Print the optimal objective value
print("The optimal value is", m.objval)

# Print the optimal solutions
for i in range(num_food):
    print("Eat", food_name[i], "with amount", food[i].x)