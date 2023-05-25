import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class ChronicDiseasePredictor:
    """Chronic kidney disease predictor model"""

    def __init__(self):
        self.data_path = "./data/kidney_disease.csv"
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.columns = None
        self._load_data()
        self._train_model()

    def _load_data(self):
        """load the dataset and split to test and train"""
        dataset = pd.read_csv(self.data_path)
        self.columns = dataset.columns[:-1]
        X = dataset.drop("Class", axis=1)
        y = dataset["Class"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def _train_model(self):
        """train the model"""
        clf = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
        clf.fit(self.X_train, self.y_train)
        self.model = clf

    def model_accuracy(self):
        """calculate the accuracy and return it"""
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        return accuracy

    def predict(self, patient_info):
        """predict the new data"""
        return self.model.predict(patient_info)
