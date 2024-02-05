class ResponseBody():
    def __init__(self, status="success", data=None, message=None):
        self.status = status
        self.data = data
        self.message = message

    @staticmethod
    def generate(serializer=None, data=None, message=None):
        if data is not None:
            instance = ResponseBody(data = data, message=message)
        elif serializer is not None:
            instance = ResponseBody(data = serializer.data, message=message)
        else:
            instance = ResponseBody()
            
        return {"status":instance.status,"data":instance.data,"message":instance.message}
    