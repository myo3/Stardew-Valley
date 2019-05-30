from gurobipy import *

MAX_LAND = 111
MAX_COST = 19253

# products = ["Sweet Gem Berry", "Cranberries", "Grapes", "Pumpkin"]
# num_products = len(products)
# profit = [2750, 693, 540, 300]
# cost = [1000, 240, 60, 100]

products = ["Cranberries", "Grapes", "Pumpkin"]
num_products = len(products)
profit = [693, 540, 300]
cost = [240, 60, 100]

m = Model()

x = m.addVars(num_products, lb=0, vtype=GRB.INTEGER, name=products)

m.addConstr(x.sum('*') <= MAX_LAND)
m.addConstr(quicksum(cost[i] * x[i] for i in range(num_products)) <= MAX_COST)

m.setObjective(quicksum(profit[i] * x[i] for i in range(num_products)), sense=GRB.MAXIMIZE)

m.optimize()


for i in range(num_products):
	print(products[i] + ": {}".format(m.x[i]))

print("Profit: {}".format(m.ObjVal))
