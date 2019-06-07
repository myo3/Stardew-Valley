import csv
import string

#TODO: Add documentation
class FileReader:

    def __init__(self, dataFilePath):
        self.dataFilePath = dataFilePath
        self.delimiter = '/'

    def readQualityData(subfolder, fertilizers):

        qualityPath = self.dataFilePath + self.delimiter + subfolder + self.delimiter

        fertilizerToQualityChance = {}
        for fertilizer in fertilizers:
            fertilizerToQualityChance[fertilizer] = []

        for fertilizer in fertilizers:
            with open(qualityPath + fertilizer + '.csv', 'r') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')

                next(csvReader)

                for row in csvReader:
                    row = [float(i) for i in row]
                    item = {}
                    item['regular'] = float(row[1])
                    item['silver'] = float(row[2])
                    item['gold'] = float(row[3])
                    fertilizerToQualityChance[fertilizer].append(item)

        return fertilizerToQualityChance

    def readCropData(subfolder, seasons):

        profitPath = self.dataFilePath + self.delimiter + subfolder + self.delimiter

        seasonToCropData = {}
        for season in seasons:
            seasonToCropData[season] = {}

        for season in seasons:
            with open(profitPath + season + '.csv', 'r') as csvfile:
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
                    item['growth'] = int(row[6])
                    item['regrowth'] = int(row[7])

                    seasonToCropData[season][item_name] = item

        return seasonToCropData
