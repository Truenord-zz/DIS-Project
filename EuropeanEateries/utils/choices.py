import os
import pandas as pd

# Get the absolute path of the current script
current_path = os.path.dirname(os.path.abspath(__file__))

# Go one folder back
parent_path = os.path.dirname(current_path)

# Construct the relative path to the dataset file
DATASET_PATH = os.path.join(parent_path, 'dataset/TA_restaurants_curated.csv')


def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            if isinstance(item, float):
                continue  # Skip float values
            elif isinstance(item, list):
                for cuisine in item:
                    setattr(self, str(cuisine).lower(), get_label_name(cuisine))
            else:
                setattr(self, str(item).lower(), get_label_name(item))



    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]


df = pd.read_csv(DATASET_PATH, sep=',')


 # ,Name,City,Cuisine Style,Ranking,Rating,Price Range,Number of Reviews,Reviews,URL_TA,ID_TA
RestaurantName = ModelChoices(df.Name.unique())
RestaurantCity = ModelChoices(df.City.unique()) 
RestaurantCuisineStyle = ModelChoices(df.Cuisine_Style.unique())
RestaurantRanking = ModelChoices(df.Ranking.unique())
RestaurantRating = ModelChoices(df.Rating.unique())
RestaurantPriceRange = ModelChoices(df.Price_Range.unique())
RestaurantNumberOfReviews = ModelChoices(df.Number_of_Reviews.unique())
RestaurantReviews = ModelChoices(df.Reviews.unique())
RestaurantURL_TA = ModelChoices(df.URL_TA.unique())
RestaurantID_TA = ModelChoices(df.ID_TA.unique())





UserTypeChoices = ModelChoices(['User'])

if __name__ == '__main__':
    print(df.Name.unique())
    print(RestaurantName.choices())     
