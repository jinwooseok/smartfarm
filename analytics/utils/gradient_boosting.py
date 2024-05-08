"""
GradientBoosting. CustomLinearRegression을 상속받아 구현
"""
from sklearn.ensemble import GradientBoostingRegressor
from analytics.utils.linear import CustomLinearRegression
class CustomGradientBoosting(CustomLinearRegression):
    """
    GradientBoosting 모델 클래스
    """
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        """
        매개변수
        - x_train (pd.DataFrame): 훈련 데이터의 독립변수
        - y_train (pd.Series): 훈련 데이터의 종속변수
        - sample_random_state (int): 훈련 데이터 분할 시 사용할 시드값
        - model_params (dict): 모델 초기화 시 사용할 매개변수
        """
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = GradientBoostingRegressor(**model_params)
        self.model_name = 'Gradient Boosting'