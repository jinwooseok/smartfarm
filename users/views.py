from http.client import REQUEST_ENTITY_TOO_LARGE
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import User
from argon2 import PasswordHasher, exceptions
from django.http import JsonResponse

# Create your views here.

#회원가입 버튼을 누르면 작동하는 함수
def register(request):
    if request.method == 'GET' : 
        return render(request, 'users/register.html')
    
    elif request.method == 'POST' :
        user_id=request.POST['regi_id']
        #비밀번호는 argon2의 hash함수를 사용해 db에 저장
        user_pw=request.POST['regi_pass']
        user_pw=PasswordHasher().hash(user_pw)
        
        user_name=request.POST['name']
        
        user_job=request.POST['regi_job']
        #phone에서 3개의 요소를 받기 때문에 (###,####,####) getlist로 값을 받음
        user_tel=request.POST.getlist('phone')
        user_tel = ''.join(user_tel)
        user=User(
            user_id = user_id,
            user_pw = user_pw,
            user_name = user_name,
            user_tel = user_tel,
            user_job = user_job,
        )
        user.save()
        return redirect('users:login')
 

# def login(request : HttpRequest) -> HttpResponse:
#     loginform = LoginForm()
#     context={'forms': loginform}

#     if request.method=='GET':
#         return render(request, 'users/login.html', context)

#     elif request.method=='POST':
#         loginform = LoginForm(request.POST)

#         if loginform.is_valid():
#             request.session['login_session'] = loginform.login_session
#             request.session.set_expiry(0) #set_expiry메서드는 세션만료시간을 설정합니다. 0을 넣을 경우 브라우저를 닫을 시 세션 쿠키 삭제 + DB의 만료기간은 14일로 설정됩니다.
#             return redirect('/')

#         else : 
#             context['forms'] = loginform
#             if loginform.errors:
#                 for value in loginform.errors.values():
#                     context['error'] = value
#         return render(request, 'users/login.html', context)


def login(request):
    #처음 로그인 화면으로 들어올 때는 get방식이므로 핸들링
    if request.method == "GET":
        return render(request, 'users/login.html' )

    #post방식을 받은 경우 로그인 유효성 인증 실시
    elif request.method == "POST":
        login_user_id=request.POST['id']
        login_user_pw=request.POST['password']

        try:
            user = User.objects.get(user_id=login_user_id)
        except User.DoesNotExist:
            user=None
            context = {
                'error' : '계정이 존재하지 않습니다.'
            }
            return render(request, 'users/login.html', context)
        
        try :
            PasswordHasher().verify(user.user_pw.encode(), login_user_pw.encode())
        except exceptions.VerifyMismatchError:
            user=None  
            context = {
                'error' : '비밀번호가 일치하지 않습니다.'
            }
            return render(request, 'users/login.html', context)
        
        if user != None:
            request.session['user'] = user.id
        
            # Redirect to a success page.
            return redirect('/')
            
        else:
            context = {
                'error' : '로그인에 실패하였습니다.'
            }
            return render(request, 'users/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
