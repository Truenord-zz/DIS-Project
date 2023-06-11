import os
import pandas as pd

# Get the absolute path of the current script
current_path = os.path.dirname(os.path.abspath(__file__))

# Go one folder back
parent_path = os.path.dirname(current_path)

# Construct the relative path to the dataset file
DATASET_PATH = os.path.join(parent_path, 'dataset/drugdata.csv')


def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, str(item).lower(), get_label_name(str(item)))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]



df = pd.read_csv(DATASET_PATH, sep=',')


DrugIdChoices = ModelChoices(df.id.unique())
DrugNameChoices = ModelChoices(df.name.unique())
DrugBrandChoices = ModelChoices(df.brand.unique())
#DrugPriceChoices = ModelChoices(df.price.unique())
DrugCityChoices = ModelChoices(df.city.unique())

UserTypeChoices = ModelChoices(['Pharmacist', 'Customer'])

if __name__ == '__main__':
    print(df['item'].unique())
    print(DrugNameChoices.choices())
