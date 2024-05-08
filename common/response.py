"""
Controller (views.py 파일)들에서 사용할 응답 객체를 정의합니다. 공통된 응답을 위한 장치
"""
class ResponseBody:
    """
    설명
        공통 응답 객체를 생성하는 클래스
    """
    def __init__(self, status="success", data=None, message=None):
        self.status = status
        self.data = data
        self.message = message

    @staticmethod
    def generate(serializer=None, data=None, message=None):
        """
        설명
            응답 객체를 생성하는 정적 메서드. 객체를 생성하지 않아도 호출 가능. 정적 팩토리 메서드. 입력값에 따라 내부 처리. 출력은 동일함
        
        매개변수
            serializer (Serializer): 직렬화된 데이터를 반환하는 경우 포함
            data (dict): 데이터를 반환하는 경우 포함
            message (str): 응답 메시지
        """
        if data is not None:
            instance = ResponseBody(data = data, message=message)
        elif serializer is not None:
            instance = ResponseBody(data = serializer.data, message=message)
        else:
            instance = ResponseBody()
        return {"status":instance.status,"data":instance.data,"message":instance.message}
    