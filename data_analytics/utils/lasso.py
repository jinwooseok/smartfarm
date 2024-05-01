from sklearn.linear_model import Lasso
from data_analytics.utils.linear import CustomLinearRegression
class CustomLassoRegression(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = Lasso(**model_params)
        self.model_name = 'Lasso Regression'