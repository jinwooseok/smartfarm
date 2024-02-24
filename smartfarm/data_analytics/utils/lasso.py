from sklearn.linear_model import Lasso
from .linear import CustomLinearRegression
class CustomLassoRegression(CustomLinearRegression):
    def __init__(self, x_dataset, y_dataset, sample_random_state, model_params):
        super().__init__(x_dataset, y_dataset, sample_random_state, model_params)
        self.model = Lasso(**model_params)
        self.model_name = 'Lasso Regression'