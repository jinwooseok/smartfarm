from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from .encoder import Encoder
from .linear import CustomLinearRegression
from .logistic import CustomLogisticRegression
class CustomRandomForestClassifier(CustomLogisticRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = RandomForestClassifier(**model_params)
        self.model_name = 'Random Forest Classifier'
    
class CustomRandomForestRegressor(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = RandomForestRegressor(**model_params)
        self.model_name = 'Random Forest Regressor'
    