import pandas as pd
from scipy.stats import pearsonr, pointbiserialr, chi2_contingency
from .encoder import Encoder
import numpy as np
def calculate_correlation(data, var1, var2):
    df = data.copy()
    type_var1 = df[var1].dtype
    type_var2 = df[var2].dtype
    
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=[var1, var2])
    
    if len(df[var1].value_counts())<=1 :
        return None
    elif len(df[var2].value_counts())<=1:
        return None
    
    
    if type_var1 in ['int64','float64'] and type_var2 in ['int64','float64']: # 연속형 - 연속형
        return round(pearsonr(df[var1], df[var2])[0], 6)

    elif type_var1 == 'object' and type_var2 == 'object': # 범주형 - 범주형
        df[var1] = Encoder.encode(df[var1], method='label')
        df[var2] = Encoder.encode(df[var2], method='label')        
        contingency_table = pd.crosstab(df[var1], df[var2])
        if contingency_table.shape[0]==2:
            correct=False
        else:
            correct=True
        chi2 = chi2_contingency(contingency_table, correction=correct)[0]
        
        if len(contingency_table) == 2:        # 범주 2개인 경우 phi 상관계수
            phi_coefficient = (chi2 / len(df))**0.5
            return round(phi_coefficient,6)
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

    elif (type_var1 == 'int64' and type_var2 == 'object') or (type_var1 == 'object' and type_var2 == 'int64'):
        # 연속형 - 범주형 or 범주형 - 연속형
        if type_var1 == 'int64' and type_var2 == 'object':
            var_continuous, var_categorical = var1, var2
        else:
            var_continuous, var_categorical = var2, var1
            
        df[var_categorical] = Encoder.encode(df[var_categorical], method='label')
        print(round(pointbiserialr(df[var_continuous], df[var_categorical])[0],6))
        return round(pointbiserialr(df[var_continuous], df[var_categorical])[0],6)

    else:
        return None
