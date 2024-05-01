from sklearn.svm import SVC, SVR
from data_analytics.utils.linear import CustomLinearRegression
from data_analytics.utils.logistic import CustomLogisticRegression

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
        
        