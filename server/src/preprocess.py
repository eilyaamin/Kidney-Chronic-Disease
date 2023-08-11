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
        self.feature_encoders = {}
        self.scaler = None
        self.translation_dict = {
            "id": "Identifier or unique record identifier",
            "age": "Age of the patient",
            "bp": "Blood pressure",
            "sg": "Specific gravity",
            "al": "Albumin",
            "su": "Sugar",
            "rbc": "Red blood cells",
            "pc": "Pus cell",
            "pcc": "Pus cell clumps",
            "ba": "Bacteria",
            "bgr": "Blood glucose random",
            "bu": "Blood urea",
            "sc": "Serum creatinine",
            "sod": "Sodium",
            "pot": "Potassium",
            "hemo": "Hemoglobin",
            "pcv": "Packed cell volume",
            "wc": "White blood cell count",
            "rc": "Red blood cell count",
            "htn": "Hypertension",
            "dm": "Diabetes mellitus",
            "cad": "Coronary artery disease",
            "appet": "Appetite",
            "pe": "Pedal edema",
            "ane": "Anemia",
        }
        self._load_data(self.data_path)
        self._handle_missing_values()
        self._normalize_numerical_columns()
        self._encode_categorical_columns()
        self._perform_feature_selection()
        self._split_numerical_categorical()
        # self.dataset.to_csv("NEW_DATASET.csv", index=False)

    def _load_data(self, file_path):
        self.dataset = pd.read_csv(file_path)

    def load_data(self, file_path):
        return pd.read_csv(file_path)

    def _handle_missing_values(self):
        self.dataset = self.dataset.drop("id", axis=1)
        self.dataset = self.dataset.applymap(lambda cell_value: cell_value.replace("\t", "").replace("?", "") if isinstance(cell_value, str) else cell_value)

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
        self.scaler = scaler

    def _encode_categorical_columns(self):
        le = LabelEncoder()
        label_mapping = {"ckd": 1, "notckd": 0}
        le.classes_ = pd.Series(list(label_mapping.keys()))
        self.dataset["classification"] = self.dataset["classification"].str.strip()
        self.dataset["classification"] = le.transform(self.dataset["classification"])

        for column in self.categorical_cols:
            label_encoder = LabelEncoder()
            encoded_values = label_encoder.fit_transform(self.dataset[column])
            self.dataset[column] = encoded_values

            # Store the encoder for later use
            self.feature_encoders[column] = label_encoder

    def _perform_feature_selection(self):
        X = self.dataset.drop("classification", axis=1)
        y = self.dataset["classification"]
        selector = SelectKBest(f_classif, k=23)
        X_new = selector.fit_transform(X, y)

        selected_feature_indices = selector.get_support(indices=True)
        selected_feature_names = X.columns[selected_feature_indices]

        self.dataset = pd.concat(
            [pd.DataFrame(X_new, columns=selected_feature_names), y], axis=1
        )

    def _split_numerical_categorical(self):
        data = self.dataset.copy()
        
        text_columns = []
        number_columns = []
        
        for col in data.columns:
            if col == "classification":
                continue
            
            # Check if any element can be converted to a number
            has_numbers = any(pd.to_numeric(data[col], errors='coerce').notna())
            
            if has_numbers:
                # If column has numbers, consider it numeric
                numeric_col = pd.to_numeric(data[col], errors='coerce')
                number_columns.append({
                    "name": self.translate_token_to_word(col),
                    "type": "number",
                    "min": numeric_col.min(),
                    "max": numeric_col.max()
                })
            else:
                # If column doesn't have numbers, consider it categorical
                categories = list(set([val.strip() for val in data[col].unique().tolist()]))
                text_columns.append({
                    "name": self.translate_token_to_word(col),
                    "type": "text",
                    "categories": categories
                })
        
        # Combine text_columns and number_columns, with text types first
        self.columns = text_columns + number_columns

    def get_data(self):
        """returns preprocessed data"""
        return self.dataset

    def get_columns(self):
        """Returns the list of preprocessed columns/features"""
        return self.columns

    def translate_token_to_word(self, token):
        """Returns the word corresponding to the token"""
        if token in self.translation_dict:
            return self.translation_dict[token]
        else:
            return token
        
    def translate_word_to_token(self, word):
        """Returns the token corresponding to the word"""
        reverse_translation_dict = {v: k for k, v in self.translation_dict.items()}

        if word in reverse_translation_dict:
            return reverse_translation_dict[word]
        else:
            return word

    def preprocess_new_record(self, new_record):
        """Preprocesses a new record to make it prediction-ready"""
        try:
            # Apply the same preprocessing steps as the original dataset
            print(new_record.columns)
            new_df = self._normalize_numerical_columns_for_new_data(new_record)


            # Apply stored encoders to categorical columns
            for column in self.categorical_cols:
                if column in new_record.columns:
                    print("for loop")
                    encoded_values = self.apply_feature_encoder(column, new_df[column])
                    new_df[column] = encoded_values
            return new_df

        except Exception as e:
            print(f"Error during preprocessing new record: {str(e)}")
            return None

    def _normalize_numerical_columns_for_new_data(self, new_df):
        try:
            numerical_columns = self.dataset.select_dtypes(
                include=["int64", "float64"]
            ).columns.drop("classification")
            new_df[numerical_columns] = self.scaler.fit_transform(
                new_df[numerical_columns]
            )
            return new_df
        except Exception as e:
            print(f"Error during _normalize_numerical_columns_for_new_data: {str(e)}")
            return None

    def apply_feature_encoder(self, feature_name, values):
        """Apply the stored encoder to new values"""
        try:
            encoder = self.feature_encoders[feature_name]
            if encoder:
                return encoder.transform(values)
            else:
                return values
        except Exception as e:
            print(f"Error during apply_feature_encoder: {str(e)}")
            return None
