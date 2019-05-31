from gurobipy import *
import csv
import string

dataFilePath = 'Data/'

qualities = ['regular', 'silver', 'gold']
seasons = ['spring', 'summer', 'fall', 'winter']
fertilizers = ['none', 'basic', 'quality']

noneQualityChance = []
basicQualityChance = []
qualityQualityChance = []

springCropProfit = {}
summerCropProfit = {}
fallCropProfit = {}
winterCropProfit = {}

def readData():
	'''
	Reads quality chance and crop profit data from csv file.
	'''
	cropQualityPath = dataFilePath + 'Quality Crop Frequency/'

	for fertilizer in fertilizers:
		with open(cropQualityPath + fertilizer + '.csv', 'r') as csvfile:
			csvReader = csv.reader(csvfile, delimiter=',')

			next(csvReader)

			for row in csvReader:
				row = [float(i) for i in row]
				item = {}
				item['regular'] = float(row[1])
				item['silver'] = float(row[2])
				item['gold'] = float(row[3])
				eval(fertilizer + 'QualityChance').append(item)

	cropProfitPath = dataFilePath + 'Crop Profit/'

	for season in seasons:
		with open(cropProfitPath + season + '.csv', 'r') as csvfile:
			csvReader = csv.reader(csvfile, delimiter=',')

			next(csvReader)

			for row in csvReader:
				item_name = string.capwords(row[0].strip().lower())
				item = {}
				item['regular'] = float(row[1])
				item['silver'] = float(row[2])
				item['gold'] = float(row[3])
				item['cost'] = float(row[4])
				item['location'] = string.capwords(row[5].strip().lower())

				eval(season + 'CropProfit')[item_name] = item

def getCropQualityChance(level=0, boost=0, fertilizer='none'):
	'''
	Get the chance of recieving each quality of crop depending on 
	farming level and fertilizer.

	Parameters:
		level : integer, optional
			Farming level between 0-10. Default level 0.
		boost : integer, optional
			Farming level boost 0-3. Default boost 0.
		fertilizer: string, optional
			Fertilizer used on patch. One of 'none', 'basic', or 'quality'.
			Default fertilizer 'none'.
	
	Return:
		quality : list
			Percentage chance of getting each quality of the item
	'''
	assert level >= 0 and level <= 10, "Invalid farming level."
	assert boost >= 0 and boost <= 3, "Invalid boost amount."
	assert fertilizer == 'none' or fertilizer == 'basic' or fertilizer == 'quality', "Invalid fertilizer type."

	totalLevel = level + boost

	quality = eval(fertilizer + 'QualityChance')[totalLevel]

	return quality

# TODO: NEED TO FACTOR IN YIELD PER CROP
def getExpectedProfit(season, crop, level=0, boost=0, fertilizer='none'):
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
	assert season in seasons, "Invalid season."

	crop = string.capwords(crop.strip().lower())
	cropData = {}
	try:
		cropData = eval(season + 'CropProfit')[crop]
	except:
		print("Invalid crop name.")

	assert level >= 0 and level <= 10, "Invalid farming level."
	assert boost >= 0 and boost <= 3, "Invalid boost amount."
	assert fertilizer == 'none' or fertilizer == 'basic' or fertilizer == 'quality', "Invalid fertilizer type."

	totalLevel = level + boost

	qualityData = eval(fertilizer + 'QualityChance')[totalLevel]

	profit = 0

	for quality in qualities:
		profit += cropData[quality] * qualityData[quality]

	profit -= cropData['cost']

	return profit

def getCropCosts(season, crop):
	'''
	Get the cost of the seed for a crop.
	'''
	assert season in seasons, "Invalid season."

	crop = string.capwords(crop.strip().lower())
	cropData = {}
	try:
		cropData = eval(season + 'CropProfit')[crop]
	except:
		print("Invalid crop name.")

	cost = cropData['cost']

	return cost

readData()


MAX_LAND = 111
MAX_COST = 19253

# products = ["Sweet Gem Berry", "Cranberries", "Grapes", "Pumpkin"]
# num_products = len(products)
# profit = [2750, 693, 540, 300]
# cost = [1000, 240, 60, 100]
season = 'fall'
products = ["Cranberries", "Grape", "Pumpkin"]
num_products = len(products)
profit = [getExpectedProfit(season, crop) for crop in products]
cost = [getCropCosts(season, crop) for crop in products]

print(profit)
print(cost)

m = Model()

x = m.addVars(num_products, lb=0, vtype=GRB.INTEGER, name=products)

m.addConstr(x.sum('*') <= MAX_LAND)
m.addConstr(quicksum(cost[i] * x[i] for i in range(num_products)) <= MAX_COST)

m.setObjective(quicksum(profit[i] * x[i] for i in range(num_products)), sense=GRB.MAXIMIZE)

m.optimize()


for i in range(num_products):
	print(products[i] + ": {}".format(m.x[i]))

print("Profit: {}".format(m.ObjVal))
