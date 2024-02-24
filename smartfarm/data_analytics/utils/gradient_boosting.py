from sklearn.ensemble import GradientBoostingRegressor
from .linear import CustomLinearRegression
class CustomGradientBoosting(CustomLinearRegression):
    def __init__(self, x_dataset, y_dataset, sample_random_state, model_params):
        super().__init__(x_dataset, y_dataset, sample_random_state, model_params)
        self.model = GradientBoostingRegressor(**model_params)
        self.model_name = 'Gradient Boosting'