from sklearn.linear_model import Lasso
from .linear import CustomLinearRegression
class CustomLassoRegression(CustomLinearRegression):
    def __init__(self, x_dataset, y_dataset, random_state, alpha=1.0):
        super().__init__(x_dataset, y_dataset, random_state)
        self.model = Lasso(alpha=alpha)
        self.alpha = alpha
        self.model_name = 'Lasso Regression'
    def meta(self):
        meta = super().meta()
        meta['alpha'] = self.alpha
        return meta