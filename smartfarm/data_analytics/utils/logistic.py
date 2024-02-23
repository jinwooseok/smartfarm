from sklearn.linear_model import LogisticRegression
from .linear import CustomLinearRegression

class CustomLogisticRegression(CustomLinearRegression):
    def __init__(self, x_dataset, y_dataset, random_state):
        super().__init__(x_dataset, y_dataset, random_state)
        self.model = LogisticRegression()
        self.model_name = 'Logistic Regression'