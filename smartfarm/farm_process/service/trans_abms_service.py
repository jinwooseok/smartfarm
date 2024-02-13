import pandas as pd
from ..utils.process import ETLProcessFactory
from ...file.service.file_save_service import FileSaveService
from ...file_data.service.get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ..exceptions.exceptions import StartIndexException
class TransABMSService():
    def __init__(self, user, columns, new_file_name, date_column, start_index, file_root):
        self.user = user
        self.columns = columns
        self.new_file_name = new_file_name
        self.date_column = date_column
        self.start_index = start_index
        self.file_type = "env"
        self.interval = "hourly"
        self.file_root = file_root
    
    @classmethod
    def from_serializer(cls, serializer, user) -> "TransABMSService":
        return cls(user, serializer.validated_data['columns'], serializer.validated_data['newFileName']
                   , serializer.validated_data['date'], serializer.validated_data['startIndex'], serializer.get_file_object(user).file_root)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        #데이터프레임 윗부분 자르기
        if self.start_index < 1 or self.start_index > len(df):
            raise StartIndexException()
            
        df = df.iloc[self.start_index-1:]
        
        after_list = [column[1] for column in self.columns]
        var_list = []
        for before_name, after_name in self.columns:
            dic = {}
            if before_name not in df.columns:
                continue
            df.rename(columns={before_name: after_name}, inplace=True)
            #그냥 농업데이터 처리 그대로 가져오고 모든 라인 전체 평균으로 처리
            if after_name in ["내부온도", "내부습도"]:
                #전체평균 ,주간평균, 야간평균, 전체최저, 전체최고 생성
                dic[after_name] = [["전체", "평균"], ["주간", "평균"], ["야간", "평균"], ["전체", "최소"], ["전체", "최대"]]
            elif after_name in ["외부온도"]:
                #전체평균 ,주간평균, 야간평균 생성
                dic[after_name] = [["전체", "평균"], ["주간", "평균"], ["야간", "평균"]]
            elif after_name in ["일시"]:
                continue
            else:
                dic[after_name] =[["전체", "평균"]]
            var_list.append(dic)

        #프로세스 선정
        process_factory = ETLProcessFactory(df, self.file_type, self.date_column, self.interval, var = var_list)
        #정적 메서드 핸들러
        result = process_factory.handler()
        #그렇게 컬럼 데이터를 만들고 농업전처리를 실행..하지만 이름은 맞춰줘야한다..
        #날짜 > 일시, 전체평균 붙은 경우 전체평균 빼기, 전체최소****>**** 최저, 전체최대****>**** 최고, 주간평균****>**** 주간, 야간평균****>**** 야간
        for column in result.columns:
            result.rename(columns={column:self.naming_variable(column)}, inplace=True)
        for column in after_list:
            if column not in result.columns:
                result[column] = pd.Series(dtype=float)
        result = result[after_list]
        FileSaveService(self.user, self.new_file_name, result, statuses=2).execute()
    
    @staticmethod
    def naming_variable(column_name):
        if "날짜" in column_name:
            return "일시"
        elif "전체평균" in column_name:
            return column_name.replace("전체평균", "")
        elif "전체최소" in column_name:
            return column_name.replace("전체최소", "") + " 최저"
        elif "전체최대" in column_name:
            return column_name.replace("전체최대", "") + " 최고"
        elif "주간평균" in column_name:
            return column_name.replace("주간평균", "") + " 주간"
        elif "야간평균" in column_name:
            return column_name.replace("야간평균", "") + " 야간"