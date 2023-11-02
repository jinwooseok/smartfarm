from .models import File
def findFileObjectByUserId(user_id):
    return File.objects.filter(user_id=user_id) 

