from sklearn.ensemble import GradientBoostingRegressor
from .linear import CustomLinearRegression
class CustomGradientBoosting(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = GradientBoostingRegressor(**model_params)
        self.model_name = 'Gradient Boosting'