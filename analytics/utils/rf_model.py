"""
Random Forest Model(분류, 회귀) 클래스. 각각 CustomLogisticRegression, CustomLinearRegression을 상속받아 구현되었다.
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from analytics.utils.linear import CustomLinearRegression
from analytics.utils.logistic import CustomLogisticRegression
class CustomRandomForestClassifier(CustomLogisticRegression):
    """
    Random Forest Classifier 모델 클래스
    """
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = RandomForestClassifier(**model_params)
        self.model_name = 'Random Forest Classifier'

class CustomRandomForestRegressor(CustomLinearRegression):
    """
    Random Forest Regressor 모델 클래스
    """
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = RandomForestRegressor(**model_params)
        self.model_name = 'Random Forest Regressor'
