import pandas as pd
#---------------모델 import---------------------
from ..models import File

#--------------캐시 처리 라이브러리-------------
from django.core.cache import cache
class JsonProcess:
    def jsonToDf(json):
        data = pd.DataFrame(json)
        return data

def dataJoiner(df1, df2, left_key, right_key):
    joinedData = pd.merge(df1, df2, left_on=left_key, right_on=right_key, how='left')
    return joinedData
