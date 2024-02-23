import pandas as pd
from scipy.stats import pearsonr, pointbiserialr, chi2_contingency, cramer_v

def calculate_correlation(df, var1, var2):
    type_var1 = df[var1].dtype
    type_var2 = df[var2].dtype
    
    if type_var1 == 'int64' and type_var2 == 'int64':
        # 연속형 - 연속형
        correlation_coefficient, _ = pearsonr(df[var1], df[var2])
        return correlation_coefficient

    elif type_var1 == 'object' and type_var2 == 'object':
        # 범주형 - 범주형
        contingency_table = pd.crosstab(df[var1], df[var2])
        chi2, _, _, _ = chi2_contingency(contingency_table)
        
        if len(contingency_table) == 2:
            # 범주 2개인 경우 phi 상관계수
            phi_coefficient = (chi2 / len(df))**0.5
            return phi_coefficient
        else:
            # 범주 3개 이상인 경우 cramer's v
            cramer_v_coefficient = (chi2 / (len(df) * (min(len(contingency_table), len(contingency_table.columns)) - 1)))**0.5
            return cramer_v_coefficient

    elif (type_var1 == 'int64' and type_var2 == 'object') or (type_var1 == 'object' and type_var2 == 'int64'):
        # 연속형 - 범주형 or 범주형 - 연속형
        if type_var1 == 'int64' and type_var2 == 'object':
            var_continuous, var_categorical = var1, var2
        else:
            var_continuous, var_categorical = var2, var1

        point_biserial_coefficient, _ = pointbiserialr(df[var_continuous], df[var_categorical])
        return point_biserial_coefficient

    else:
        return None