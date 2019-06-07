import FileReader
import DataReader
import Model

fertilizers = ['none', 'basic', 'quality']
seasons = ['spring', 'summer', 'fall', 'winter']

reader = FileReader('Data')

fertilizerToQualityChance = reader.readQualityData('Quality', fertilizers)
seasonToCropData = reader.readCropData('Crop', seasons)

data = DataReader(fertilizerToQualityChance, seasonToCropData)

model = Model(data)
solution = model.getSolution(maxPlots=111, maxGold=19253, season='fall')
Model.printSolution(solution)
