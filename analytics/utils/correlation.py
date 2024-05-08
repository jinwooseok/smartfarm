"""
상관계수를 계산하는 함수를 정의한 파일
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, pointbiserialr, chi2_contingency
from analytics.utils.encoder import Encoder

def calculate_correlation(data:pd.DataFrame, var1:str, var2:str) -> float|None:
    """
    설명
    - 두 변수의 상관계수를 계산하는 함수
    - 두 변수가 연속형 - 연속형인 경우 피어슨 상관계수를 계산
    - 두 변수가 범주형 - 범주형인 경우 phi 상관계수를 계산. 범주가 3개 이상인 경우 Cramer's V를 계산
    - 두 변수가 연속형 - 범주형, 범주형 - 연속형인 경우 포인트 pointbiserial 상관계수를 계산
    
    매개변수
    - data (DataFrame): 전체 데이터프레임
    - var1 (str): 변수1
    - var2 (str): 변수2
    
    반환값
    - 상관계수 (float), 상관계수를 계산할 수 없는 경우 None 반환
    """
    # 데이터 전처리
    df = data.copy()
    type_var1 = df[var1].dtype
    type_var2 = df[var2].dtype
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=[var1, var2])

    # 변수의 값이 1개 이하인 경우 상관계수 계산 불가
    if len(df[var1].value_counts())<=1 :
        return None
    elif len(df[var2].value_counts())<=1:
        return None

    # 1. 연속형 - 연속형인 경우 피어슨 상관계수
    if type_var1 in ['int64','float64'] and type_var2 in ['int64','float64']: # 연속형 - 연속형
        return round(pearsonr(df[var1], df[var2])[0], 6)

    # 2. 범주형 - 범주형인 경우 phi 상관계수 (범주가 3개 이상인 경우 Cramer's V)
    elif type_var1 == 'object' and type_var2 == 'object':
        df[var1] = Encoder.encode(df[var1], method='label')
        df[var2] = Encoder.encode(df[var2], method='label')
        contingency_table = pd.crosstab(df[var1], df[var2])
        if contingency_table.shape[0]==2:
            correct=False
        else:
            correct=True
        chi2 = chi2_contingency(contingency_table, correction=correct)[0]
        # phi 계수 계산
        if len(contingency_table) == 2:
            phi_coefficient = (chi2 / len(df))**0.5
            return round(phi_coefficient,6)
        # Cramer's V 계수 계산
        else:   
            n = sum(contingency_table.sum())
            phi2 = chi2/n
            r,k = contingency_table.shape
            phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))    
            if phi2corr == 0:
                return 0
            rcorr = r - ((r-1)**2)/(n-1)
            kcorr = k - ((k-1)**2)/(n-1)
            result=np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))
            return round(result,6)

    # 3. 연속형 - 범주형 or 범주형 - 연속형인 경우
    elif (type_var1 == 'int64' and type_var2 == 'object') or (type_var1 == 'object' and type_var2 == 'int64'):
        if type_var1 == 'int64' and type_var2 == 'object':
            var_continuous, var_categorical = var1, var2
        else:
            var_continuous, var_categorical = var2, var1
        # 인코딩 진행 후 pointbiserial 상관계수 계산
        df[var_categorical] = Encoder.encode(df[var_categorical], method='label')
        return round(pointbiserialr(df[var_continuous], df[var_categorical])[0],6)
    
    # 4. 그 외의 경우
    else:
        return None
