from sklearn.linear_model import Ridge
from .linear import CustomLinearRegression

class CustomRidgeRegression(CustomLinearRegression):
    def __init__(self, x_dataset, y_dataset, random_state, alpha=1.0):
        super().__init__(x_dataset, y_dataset, random_state)
        self.model = Ridge(alpha=alpha)
        self.alpha = alpha
        self.model_name = 'Ridge Regression'
        
    def meta(self):
        meta = super().meta()
        meta['alpha'] = self.alpha
        return meta