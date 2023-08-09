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
        self.columns = []
        self.label = None
        self.categorical_cols = None
        self.numerical_cols = None
        self._load_data(self.data_path)
        self._normalize_numerical_columns()
        self._handle_missing_values()
        self._encode_categorical_columns()
        self._split_numerical_categorical()
        self._perform_feature_selection()
        self.testing

    def _load_data(self, file_path):
        self.dataset = pd.read_csv(file_path)

    def _handle_missing_values(self):
        self.dataset = self.dataset.drop("id", axis=1)

        self.numerical_cols = self.dataset.select_dtypes(
            include=["float64", "int64"]
        ).columns

        imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
        imputer.fit(self.dataset[self.numerical_cols])
        self.dataset[self.numerical_cols] = imputer.transform(
            self.dataset[self.numerical_cols]
        ).round(3)

        self.categorical_cols = self.dataset.select_dtypes(include=["object"]).columns
        self.dataset[self.categorical_cols] = self.dataset[
            self.categorical_cols
        ].fillna(self.dataset[self.categorical_cols].mode().iloc[0])

    def _normalize_numerical_columns(self):
        numerical_columns = self.dataset.select_dtypes(
            include=["int64", "float64"]
        ).columns

        scaler = MinMaxScaler()
        self.dataset[numerical_columns] = scaler.fit_transform(
            self.dataset[numerical_columns]
        )

    def _encode_categorical_columns(self):
        le = LabelEncoder()
        label_mapping = {"ckd": 1, "notckd": 0}
        le.classes_ = pd.Series(list(label_mapping.keys()))
        self.dataset["classification"] = self.dataset["classification"].str.strip()
        self.dataset["classification"] = le.transform(self.dataset["classification"])

        for column in self.categorical_cols:
            label_encoder = LabelEncoder()
            self.dataset[column] = label_encoder.fit_transform(self.dataset[column])

    def _split_numerical_categorical(self):
        self.numerical_data = self.dataset[self.numerical_cols]
        self.categorical_data = self.dataset[self.categorical_cols]

    def _perform_feature_selection(self):
        X = self.dataset.drop("classification", axis=1)
        y = self.dataset["classification"]
        selector = SelectKBest(f_classif, k=15)
        X_new = selector.fit_transform(X, y)

        selected_feature_indices = selector.get_support(indices=True)
        selected_feature_names = X.columns[selected_feature_indices]

        self.selected_features = selected_feature_names

        self.dataset = pd.concat(
            [pd.DataFrame(X_new, columns=selected_feature_names), y], axis=1
        )

        for col in self.dataset.columns:
            if col == "classification":
                continue
            if col in self.categorical_cols:
                self.columns.append({"name": col, "type": "text"})
            if col in self.numerical_cols:
                self.columns.append({"name": col, "type": "number"})

    def get_selected_features(self):
        """returns the list of selected features after feature selection"""
        return self.selected_features

    def get_data(self):
        """returns preprocessed data"""
        return self.dataset

    def get_columns(self):
        """Returns the list of preprocessed columns/features"""
        return self.columns

    # def testing(self):
    #     # Sample column names
    #     column_names = [
    #         "age", "bp", "sg", "alb", "su", "rbc", "pc", "pcc", "ba", "bgr", "bu", "sc", "sod", "pot",
    #         "hemo", "pcv", "wbcc", "rbcc", "htn", "dm", "cad", "appet", "pe", "ane", "classification"
    #     ]

    #     # Tokenize and POS tag each column name
    #     tokenized_names = [word_tokenize(name) for name in column_names]
    #     pos_tags = [pos_tag(tokens) for tokens in tokenized_names]

    #     # Display the POS tags for each column name
    #     for name, tags in zip(column_names, pos_tags):
    #         print(name, tags)
