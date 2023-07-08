import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, chi2



class Preprocessor:
    """class to load and preprocess the data"""
    def __init__(self):
        self.data_path = "./src/data/kidney_disease.csv"
        self.dataset = None
        self.columns = None
        self.lable = None
        self.categorical_cols = None
        self.numerical_cols = None
        self._load_data(self.data_path)
        self._handle_missing_values()
        self._handle_standardization()
        self._preform_feature_selection()

    def _load_data(self, file_path):
        self.dataset = pd.read_csv(file_path)

    def _handle_missing_values(self):
        # Handle missing values
        self.dataset.replace('\t?', np.nan, inplace=True)
        # Handling missing values in numerical columns
        self.numerical_cols = self.dataset.select_dtypes(include=['float64', 'int64']).columns
        self.dataset[self.numerical_cols] = self.dataset[self.numerical_cols].fillna(self.dataset[self.numerical_cols].mean())
        # Handling missing values in categorical columns
        self.categorical_cols = self.dataset.select_dtypes(include=['object']).columns
        self.dataset[self.categorical_cols] = self.dataset[self.categorical_cols].fillna(self.dataset[self.categorical_cols].mode().iloc[0])

    def _handle_standardization(self):
        # Drop irrelevant columns (if any)
        self.dataset.drop(['id'], axis=1)
        # Encode categorical variables
        label_encoder = LabelEncoder()
        for column in self.categorical_cols:
            self.dataset[column] = label_encoder.fit_transform(self.dataset[column].astype(str))
        # Convert categorical columns to appropriate data types
        for column in self.categorical_cols:
            self.dataset[column] = self.dataset[column].astype('category')
        # Normalize numerical columns
        scaler = StandardScaler()
        self.dataset[self.numerical_cols] = scaler.fit_transform(self.dataset[self.numerical_cols])

    def _preform_feature_selection(self):
        # Perform feature selection
        self.columns = self.dataset.drop('classification', axis=1)
        self.lable = self.dataset['classification']
        selector = SelectKBest(chi2, k=10)
        selector.fit_transform(self.columns, self.lable)

    def get_data(self):
        """returns preprocessed data"""
        return self.columns, self.lable
