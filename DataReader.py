import string

#TODO: Add documentation
class DataReader:

    def __init__(self, fertilizerToQualityChance, seasonToCropData):
        self.fertilizerToQualityChance = fertilizerToQualityChance
        self.seasonToCropData = seasonToCropData

    def getCropQualityChance(self, level=0, boost=0, fertilizer='none'):
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
            quality : string dict
                Percentage chance of getting each quality of the item

                Keys:

                'regular': float
                    Percent chance in decimal for regular crops

                'silver': float
                    Percent chance in decimal for silver crops

                'gold': float
                    Percent chance in decimal for gold crops

        '''
        assert level >= 0 and level <= 10, "Invalid farming level."
        assert boost >= 0 and boost <= 3, "Invalid boost amount."
        assert fertilizer in self.fertilizerToQualityChance.keys(), "Invalid fertilizer type."

        totalLevel = level + boost

        quality = self.fertilizerToQualityChance[fertilizer][totalLevel]

        return quality

    def getCropData(self, season, crop):
        '''
        Get crop data from season and crop name

        Parameters
            season : string
                Season in which crop is grown. One of 'spring', 'summer', 'fall', or 'winter'
            crop : string
                Name of crop to get expected profit.

        Return:
            cropData: string dict
                Information about crop.

                Keys:

                'regular': float
                    Sell price for regular crop

                'silver': float
                    Sell price for silver crop

                'gold': float
                    Sell price for gold crop

                'cost': float
                    Minimum cost to purchase crop

                'location': string
                    Location where can buy crop at minium cost (in caps)

                'growth': int
                    Number of days it takes for crop to harvest

                'regrowth': int
                    Number of days it takes for crop to regrow after first harvest

        '''
        assert season in self.seasonToCropData.keys(), "Invalid season."
        assert crop in self.seasonToCropData[season].keys(), "Crop: " + crop + " does not exist for season: " + season + "."

        crop = string.capwords(crop.strip().lower())
        cropData = self.seasonToCropData[season][crop]

        return cropData

    def getCropCosts(self, season, crop):
        '''
        Get the cost of the seed for a crop.
        '''
        cropData = self.getCropData(season, crop)

        cost = cropData['cost']

        return cost
