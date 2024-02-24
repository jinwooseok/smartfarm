from sklearn.linear_model import ElasticNet
from .linear import CustomLinearRegression
class CustomElasticNet(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = ElasticNet(**model_params)
        self.model_name = 'ElasticNet'
