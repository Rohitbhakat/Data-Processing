import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class DataCorrection:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def fill_missing(self, fill_values: dict):
        for column, value in fill_values.items():
            self.df[column].fillna(value, inplace=True)
        return self.df

    def normalize(self, columns):
        scaler = MinMaxScaler()
        self.df[columns] = scaler.fit_transform(self.df[columns])
        return self.df
