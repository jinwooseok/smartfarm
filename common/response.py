class ResponseBody():
    def __init__(self, status="success", data=None):
        self.status = status
        self.data = data

    @staticmethod
    def generate(serializer=None):
        if serializer is not None:
            instance = ResponseBody(data = serializer.data)
        else:
            instance = ResponseBody()
            
        return {"status":instance.status,"data":instance.data}
    