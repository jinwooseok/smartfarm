from ..models import Temp, File
from ..exceptions import *
def get_temp_by_file_id_status_id(file_id, status_id):
    try:
        return Temp.objects.get(file_id=file_id, statuses=status_id)
    except:
        raise TempNotFoundException()

def get_temp_or_none_by_file_id_status_id(file_id, status_id):
    try:
        return Temp.objects.get(file_id=file_id, statuses=status_id)
    except:
        return None
    
def get_file_by_user_file_title(user_id, file_title):
    try:
        return File.objects.get(user=user_id, file_title=file_title)
    except:
        raise FileNotFoundException()

def filter_file_by_user(user_id):
    return File.objects.filter(user=user_id) 

def exist_file_by_user_file_title(user_id, file_title):
    return File.objects.filter(user=user_id, file_title=file_title).exists() 

