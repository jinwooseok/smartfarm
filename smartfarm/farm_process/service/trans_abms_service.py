import pandas as pd
from ..utils.process import ETLProcessFactory
class TransABMSService():
    def __init__(self, user, columns, new_file_name, date_column, start_index):
        self.user = user
        self.columns = columns
        self.new_file_name = new_file_name
        self.date_column = date_column
        self.start_index = start_index
        self.file_type = "env"
        self.interval = "hourly"
    @classmethod
    def from_serializer(cls, user, serializer):
        return cls(user, serializer.columns, serializer.new_file_name, serializer.date_column, serializer.start_index)
    
    def execute(self):
        df = pd.DataFrame()
        dic = {}
        for before_name, after_name in self.columns:
            df.rename(columns={before_name: after_name}, inplace=True)
            #그냥 농업데이터 처리 그대로 가져오고 모든 라인 전체 평균으로 처리
            if after_name in ["내부온도", "내부습도"]:
                #전체평균 ,주간평균, 야간평균, 전체최저, 전체최고 생성
                dic[after_name] = [["전체, 평균"], ["주간, 평균"], ["야간, 평균"], ["전체, 최저"], ["전체, 최고"]]
            elif after_name in ["외부온도"]:
                #전체평균 ,주간평균, 야간평균 생성
                dic[after_name] = [["전체, 평균"], ["주간, 평균"], ["야간, 평균"]]
            else:
                dic[after_name] =[["전체, 평균"]]
            #프로세스 선정
            process_factory = ETLProcessFactory(df, self.file_type, self.date_column, self.interval, var = dic)
            #정적 메서드 핸들러
            result = process_factory.handler()
                #그렇게 컬럼 데이터를 만들고 농업전처리를 실행..하지만 이름은 맞춰줘야한다..