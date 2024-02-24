from sklearn.linear_model import Ridge
from .linear import CustomLinearRegression

class CustomRidgeRegression(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = Ridge(**model_params)
        self.model_name = 'Ridge Regression'