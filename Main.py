from FileReader import FileReader
from DataReader import DataReader
from FarmModel import FarmModel

fertilizers = ['none', 'basic', 'quality']
seasons = ['spring', 'summer', 'fall', 'winter']

reader = FileReader('Data')

fertilizerToQualityChance = reader.readQualityData('Quality', fertilizers)
seasonToCropData = reader.readCropData('Crop', seasons)

data = DataReader(fertilizerToQualityChance, seasonToCropData)

model = FarmModel(data)
solution = model.getSolution(maxPlots=111, maxGold=19253, season='fall')
FarmModel.printSolution(solution)
