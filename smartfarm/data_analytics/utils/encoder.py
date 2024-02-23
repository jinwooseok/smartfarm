from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
class Encoder:
    def __init__(self):
        pass
    @staticmethod
    def encode(categorical_data, method):
        if method == "label":
            le = LabelEncoder()
        elif method == "onehot":
            le = OneHotEncoder()
        # 라벨인코더 선언 및 Fitting
        le = LabelEncoder()
        le.fit(categorical_data)

        # 인코딩한 데이터로 변환
        le_encoded = le.transform(categorical_data)

        return pd.DataFrame(le_encoded, columns = [categorical_data.name])