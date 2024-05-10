"""
라벨인코더, 원핫인코더를 사용하여 범주형 데이터를 수치형 데이터로 변환하는 클래스
"""
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
class Encoder:
    """
    설명
    - 라벨인코더, 원핫인코더를 사용하여 범주형 데이터를 수치형 데이터로 변환하는 클래스
    """
    @staticmethod
    def encode(categorical_data, method):
        """
        설명
        - 범주형 데이터를 수치형 데이터로 변환
        
        매개변수
        - categorical_data (pd.DataFrame): 범주형 데이터
        - method (str): 인코딩 방법 (label, onehot)
        
        반환값
        - 인코딩된 데이터
        """
        if method == "label":
            le = LabelEncoder()
        elif method == "onehot":
            le = OneHotEncoder()
        categorical_data = pd.DataFrame(categorical_data)
        encoded_data = le.fit_transform(categorical_data)
        if categorical_data.shape[1] == 1:
            encoded_data = encoded_data[:, 0]
        return encoded_data
