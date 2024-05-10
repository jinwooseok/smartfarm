"""
SVM(분류, 회귀) 클래스 정의
"""
from sklearn.svm import SVC, SVR
from analytics.utils.linear import CustomLinearRegression
from analytics.utils.logistic import CustomLogisticRegression

class CustomSVC(CustomLogisticRegression):
    """
    SVM Classifier 모델 클래스
    """
    def __init__(self, x_train, y_train, random_state, model_params):
        super().__init__(x_train, y_train, random_state, model_params)
        self.model = SVC(**model_params)
        self.model_name = 'SVC'

class CustomSVR(CustomLinearRegression):
    """
    SVM Regressor 모델 클래스
    """
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = SVR(**model_params)
        self.model_name = 'SVR'

        