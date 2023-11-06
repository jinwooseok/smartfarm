from .models import File
def findFileObjectListByUserId(user_id):
    return File.objects.filter(user_id=user_id) 

def findFileObjectByUserIdFileTitle(user_id, file_title):
    return File.objects.get(user_id=user_id, file_title=file_title)

def findFileObjectListByUserIdFileTitle(user_id, file_title):
    return File.objects.filter(user_id=user_id, file_title=file_title)