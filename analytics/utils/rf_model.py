from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from analytics.utils.linear import CustomLinearRegression
from analytics.utils.logistic import CustomLogisticRegression
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
    