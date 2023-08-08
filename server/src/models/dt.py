from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from src.preprocess import Preprocessor


class DecisionTree:
    """Decision Tree Classifier model"""

    def __init__(self):
        self.name = "Decision Tree"
        self.description = "Decision Tree: Tree-based predictive model using recursive feature partitioning."
        self.preprocessor = Preprocessor()
        self.model = DecisionTreeClassifier()
        self.accuracy = 0
        self._train()

    def _train(self):
        """Trains the model and returns the accuracy"""
        data = self.preprocessor.get_data()
        X = data.drop("classification", axis=1)
        y = data["classification"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.accuracy = accuracy.round(2) * 100

    def get_accuracy(self):
        """Returns the accuracy"""
        return self.accuracy

    def predict(self, new_data):
        """Returns the predictions"""
        predictions = self.model.predict(new_data)
        return predictions
