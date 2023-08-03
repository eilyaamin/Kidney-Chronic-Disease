import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder



class Preprocessor:
    """class to load and preprocess the data"""
    def __init__(self):
        self.data_path = "./src/data/kidney_disease.csv"
        self.dataset = None
        self.columns = None
        self.label = None
        self.categorical_cols = None
        self.numerical_cols = None
        self._load_data(self.data_path)
        self._handle_missing_values()
        # self._handle_standardization()
        # self._preform_feature_selection()
        self.dataset.to_csv('test_dataset.csv', index=False)

    def _load_data(self, file_path):
        self.dataset = pd.read_csv(file_path)

    def _handle_missing_values(self):
        # Drop irrelevant columns (if any)
        self.dataset = self.dataset.drop('id', axis=1)
        # Handling missing values in numerical columns
        self.numerical_cols = self.dataset.select_dtypes(include=['float64', 'int64']).columns
        # self.dataset[self.numerical_cols] = self.dataset[self.numerical_cols].fillna(round(self.dataset[self.numerical_cols].mean(), 3))
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(self.dataset[self.numerical_cols])
        self.dataset[self.numerical_cols] = imputer.transform(self.dataset[self.numerical_cols]).round(3)

        # Handling missing values in categorical columns
        # self.categorical_cols = self.dataset.select_dtypes(include=['object']).columns
        # ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), self.categorical_cols)], remainder='passthrough')
        # ct.fit_transform(self.dataset)

        self.categorical_cols = self.dataset.select_dtypes(include=['object']).columns
        self.dataset[self.categorical_cols] = self.dataset[self.categorical_cols].fillna(self.dataset[self.categorical_cols].mode().iloc[0])

    def _handle_standardization(self):
        """
        Standardize numerical features and one-hot encode categorical features in a given DataFrame.

        Parameters:
            data (pandas.DataFrame): The input DataFrame containing both numerical and categorical columns.

        Returns:
            pandas.DataFrame: The standardized DataFrame with numerical and categorical columns.
        """
        # Separate numerical and categorical columns
        numerical_columns = self.dataset.select_dtypes(include=['int64', 'float64']).columns
        categorical_columns = self.dataset.select_dtypes(include=['object', 'category']).columns

        # Standardize numerical columns
        if len(numerical_columns) > 0:
            scaler = StandardScaler()
            self.dataset[numerical_columns] = scaler.fit_transform(self.dataset[numerical_columns]).round(3)

        # One-hot encode categorical columns
        if len(categorical_columns) > 0:
            encoder = OneHotEncoder()
            encoded_data = encoder.fit_transform(self.dataset[categorical_columns])
            encoded_df = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out())
            self.dataset = pd.concat([self.dataset.drop(categorical_columns, axis=1), encoded_df], axis=1)

    def _preform_feature_selection(self):
        # Perform feature selection
        self.columns = self.dataset.drop('classification', axis=1)
        self.label = self.dataset['classification']
        selector = SelectKBest(f_classif, k=10)
        selector.fit_transform(self.columns, self.label)
        print(selector.get_support())

    def get_data(self):
        """returns preprocessed data"""
        return self.columns, self.label

    def get_columns(self):
        """Returns the list of preprocessed columns/features"""
        print(self.dataset)
        return self.columns
