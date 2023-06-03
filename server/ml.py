"""Machine learning model for chronic kidney disease prediction"""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class ChronicDiseasePredictor:
    """Chronic kidney disease predictor model"""

    def __init__(self):
        self.data_path = "./data/kidney_disease.csv"
        self.model = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.columns = None
        self._load_data()
        self._train_model()

    def _load_data(self):
        """load the dataset and split to test and train"""
        dataset = pd.read_csv(self.data_path)
        self.columns = dataset.columns[:-1]
        parameters = dataset.drop("Class", axis=1)
        outcome = dataset["Class"]
        x_train, x_test, y_train, y_test = train_test_split(
            parameters, outcome, test_size=0.2, random_state=42
        )
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def _train_model(self):
        """train the model"""
        clf = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
        clf.fit(self.x_train, self.y_train)
        self.model = clf

    def model_accuracy(self):
        """calculate the accuracy and return it"""
        y_pred = self.model.predict(self.x_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        return accuracy

    def predict(self, patient_info):
        """predict the new data"""
        return self.model.predict(patient_info)
