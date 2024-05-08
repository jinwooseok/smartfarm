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
        categorical_data = pd.DataFrame(categorical_data)
        encoded_data = categorical_data.apply(lambda col: le.fit_transform(col))
        if categorical_data.shape[1] == 1:
            encoded_data = encoded_data.iloc[:, 0]
        return encoded_data
