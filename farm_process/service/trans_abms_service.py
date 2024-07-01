"""
농업데이터 전처리 서비스
"""
import pandas as pd
from farm_process.utils.process import ETLProcessFactory
from file.utils.utils import search_file_absolute_path
from file.service.file_save_service import FileSaveService
from file_data.service.get_file_data_service import GetFileDataService
from common.exceptions import *
class TransABMSService():
    """
    농업데이터 전처리 서비스 클래스
    
    메서드
    - __init__(self, user, columns, new_file_name, file_object) : 초기화 메서드
    - from_serializer(cls, serializer, user) : 직렬화 클래스로부터 객체 생성 메서드
    - execute(self) : 서비스 실행 메서드
    """
    def __init__(self, user, columns, new_file_name, file_object):
        """
        초기화 메서드. 기존 환경 데이터 처리 함수를 재활용 (ETLProcessFactory)
        
        매개변수
        - user : 사용자 객체
        - columns : 컬럼 리스트
        - new_file_name : 새로운 파일명
        - file_object : 파일 객체
        """
        self.user = user
        self.columns = columns
        self.new_file_name = new_file_name
        self.file_type = "env"
        self.interval = "hourly"
        self.file_object = file_object

    @classmethod
    def from_serializer(cls, serializer, user) -> "TransABMSService":
        """
        직렬화 클래스로부터 객체 생성 메서드
        
        매개변수
        - serializer : 직렬화 클래스
        - user : 사용자 객체
        """
        file_object = serializer.get_file_object(user)
        return cls(user
                   ,serializer.validated_data['columns']
                   ,serializer.validated_data['newFileName']
                   ,file_object)

    def execute(self):
        """
        서비스 실행 메서드
        
        서비스 로직
        1. 파일 데이터를 불러온다.
        2. 프로세스를 선정한다.
        3. 프로세스를 실행한다. (ETLProcessFactory)
        4. 결과를 저장한다. (FileSaveService)
        """
        if self.file_object.date_column is None:
            raise DateColumnException()  
        file_absolute_path = search_file_absolute_path(self.file_object.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        
        #ABMS에 적합한 변수명 리스트
        after_list = ['일시', '내부온도', '내부온도 주간', '내부온도 야간', '내부온도 최저', '내부온도 최고', '내부습도',
       '내부습도 주간', '내부습도 야간', '내부습도 최저', '내부습도 최고', '이슬점', 'CO2농도', '외부온도',
       '외부온도 주간', '외부온도 야간', '외부습도', '풍향', '풍속', '외부일사', '외부누적일사량', '외부광량',
       '내부일사', '내부광량', '감우', '포화수분', '절대습도', '수분부족분', '토양수분', '토양온도', '토양EC',
       '급액EC', '급액PH', '급액수온', '토양장력', '함수저울']
        var_list = []
        
        #변수명 변경
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
                #나머지는 전체 평균으로 처리
                dic[after_name] =[["전체", "평균"]]
            var_list.append(dic)

        #프로세스 선정 (ETLProcessFactory)
        process_factory = ETLProcessFactory(df, self.file_type, self.interval, var = var_list)
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
        
        #저장 (FileSaveService)
        FileSaveService(self.user, self.new_file_name, result, '일시', 1, statuses=2).execute()
    
    @staticmethod
    def naming_variable(column_name):
        """
        변수명 변경 메서드 -> 요구 사항에 맞도록 반환할 변수명을 변경
        """
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