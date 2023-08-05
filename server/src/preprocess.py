import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
    LabelEncoder,
    OrdinalEncoder,
    MinMaxScaler,
)
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


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
        self._normalize_numerical_columns()
        self._handle_missing_values()
        self._encode_categorical_columns()
        self._preform_feature_selection()
        self.dataset.to_csv("NEW_DATASET.csv", index=False)

    def _load_data(self, file_path):
        self.dataset = pd.read_csv(file_path)

    def _handle_missing_values(self):
        # Drop irrelevant columns (if any)
        self.dataset = self.dataset.drop("id", axis=1)
        # Handling missing values in numerical columns
        self.numerical_cols = self.dataset.select_dtypes(
            include=["float64", "int64"]
        ).columns

        imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
        imputer.fit(self.dataset[self.numerical_cols])
        self.dataset[self.numerical_cols] = imputer.transform(
            self.dataset[self.numerical_cols]
        ).round(3)

        # Handling missing values in categorical columns
        self.categorical_cols = self.dataset.select_dtypes(include=["object"]).columns
        self.dataset[self.categorical_cols] = self.dataset[
            self.categorical_cols
        ].fillna(self.dataset[self.categorical_cols].mode().iloc[0])

    def _normalize_numerical_columns(self):
        numerical_columns = self.dataset.select_dtypes(
            include=["int64", "float64"]
        ).columns

        # Use MinMaxScaler to normalize numerical columns
        scaler = MinMaxScaler()
        self.dataset[numerical_columns] = scaler.fit_transform(
            self.dataset[numerical_columns]
        )

    def _encode_categorical_columns(self):
        # Get categorical columns
        categorical_columns = self.dataset.select_dtypes(include=["object", "category"])
        # Encode label column
        le = LabelEncoder()
        label_mapping = {"ckd": 1, "notckd": 0}
        le.classes_ = pd.Series(list(label_mapping.keys()))
        self.dataset["classification"] = self.dataset["classification"].str.strip()
        self.dataset["classification"] = le.transform(self.dataset["classification"])

        # Encode categorical columns
        for column in categorical_columns:
            label_encoder = LabelEncoder()
            self.dataset[column] = label_encoder.fit_transform(self.dataset[column])

    def _preform_feature_selection(self):
        # Separate the features (X) and the target (y) from the dataset
        X = self.dataset.drop("classification", axis=1)
        y = self.dataset["classification"]

        # Perform feature selection with SelectKBest
        selector = SelectKBest(f_classif, k=14)
        X_new = selector.fit_transform(X, y)

        # Get the indices of the selected features
        selected_feature_indices = selector.get_support(indices=True)

        # Get the names of the selected features
        selected_feature_names = X.columns[selected_feature_indices]

        # Update self.dataset with the selected features
        self.dataset = pd.concat(
            [pd.DataFrame(X_new, columns=selected_feature_names), y], axis=1
        )

    def get_data(self):
        """returns preprocessed data"""
        return self.dataset

    def get_columns(self):
        """Returns the list of preprocessed columns/features"""
        data = self.dataset.drop("classification", axis=1)
        return data.columns.tolist()
