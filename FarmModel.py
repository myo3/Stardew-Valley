#TODO: Add documentation
from gurobipy import *

class FarmModel:

    def __init__(self, data):
        self.model = Model()
        self.data = data

    def getExpectedProfit(self, season, crop, level=0, boost=0, fertilizer='none'):
        '''
        Calculate the expected profit per crop based on farming level and fertilizer used.

        Parameters:
            season : string
                Season in which crop is grown. One of 'spring', 'summer', 'fall', or 'winter'
            crop : string
                Name of crop to get expected profit.
            level : integer, optional
                Farming level between 0-10. Default level 0.
            boost : integer, optional
                Farming level boost 0-3. Default boost 0.
            fertilizer : string, optional
                Fertilizer used on patch. One of 'none', 'basic', or 'quality'.
                Default fertilizer 'none'.

        Return:
            profit : float
                Expected profit of given crop at given level
        '''
        cropData = self.data.getCropData(season, crop)
        qualityData = self.data.getCropQualityChance(level, boost, fertilizer)

        profit = 0

        for quality in qualityData.keys():
            profit += cropData[quality] * qualityData[quality]

        profit -= cropData['cost']

        return profit

    def getSolution(self, maxPlots, maxGold, season):
        products = self.data.seasonToCropData[season].keys()
        num_products = len(products)
        profit = [self.getExpectedProfit(season, crop) for crop in products]
        cost = [self.data.getCropCosts(season, crop) for crop in products]

        profit = [self.getExpectedProfit(season, crop) for crop in products]
        cost = [self.data.getCropCosts(season, crop) for crop in products]

        x = self.model.addVars(num_products, lb=0, vtype=GRB.INTEGER, name=products)

        self.model.addConstr(x.sum('*') <= maxPlots)
        self.model.addConstr(quicksum(cost[i] * x[i] for i in range(num_products)) <= maxGold)

        self.model.setObjective(quicksum(profit[i] * x[i] for i in range(num_products)), sense=GRB.MAXIMIZE)

        self.model.optimize()

        solution = {"CROPS" : {}, "PROFIT" : 0.0}
        for i in range(num_products):
            if self.model.x[i] > 0:
                solution["CROPS"][products[i]] = self.model.x[i]

        solution["PROFIT"] = self.model.ObjVal

        return solution

    @staticmethod
    def printSolution(solution):
        print("Profit: {}".format(solution["PROFIT"]))

        for product, number in solution.items():
            print(product + ": {}".format(number))
