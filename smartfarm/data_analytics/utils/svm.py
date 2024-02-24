from sklearn.svm import SVC, SVR
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from .linear import CustomLinearRegression
from .logistic import CustomLogisticRegression

class CustomSVC(CustomLogisticRegression):
    def __init__(self, x_train, y_train, random_state, model_params):
        super().__init__(x_train, y_train, random_state, model_params)
        self.model = SVC(**model_params)
        self.model_name = 'SVC'
    
class CustomSVR(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = SVR(**model_params)
        self.model_name = 'SVR'
        
        