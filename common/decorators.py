'''
wraps : 데코레이터를 사용하면 함수의 이름이 변경되기 때문에 wraps를 사용하여 함수의 이름을 유지한다.
serializer_validator : serializer가 유효한지 확인하는 데코레이터
time : 시간을 측정하는 데코레이터
'''
import time
from functools import wraps
from common.validators import serializer_validator

def valid_serializer(view_func):
    '''
    설명 :
        serializer를 검증하는 데코레이터. common/validators.py의 serializer_validator를 사용하여 유효성을 검증한다
    매개변수 : 
        view_func : 함수
    반환값 : 
        wrapper : 데코레이터로 감싸고 있는 함수
    '''
    @wraps(view_func)
    def wrapper(serializer, *args, **kwargs):
        serializer = serializer_validator(serializer)
        return view_func(serializer, *args, **kwargs)
    return wrapper

def logging_time(view_func):
    '''
    설명 :
        함수 실행시간을 측정하는 데코레이터
    매개변수 : 
        view_func : 함수
    반환값 : 
        wrapper : 함수
    '''
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = view_func(*args, **kwargs)

        end_time = time.time()
        print("WorkingTime[%s]: %d sec", view_func.__name__, end_time - start_time)
        return result
    return wrapper