from http.client import REQUEST_ENTITY_TOO_LARGE
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import User
from argon2 import PasswordHasher, exceptions
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
# Create your views here.

def register(request : HttpRequest) -> HttpResponse:
    register_form = RegisterForm()
    context = {'forms': register_form}

    if request.method == 'GET' : 
        return render(request, 'users/register.html', context)
    
    elif request.method == 'POST' :
        register_form = RegisterForm(request.POST)
        if register_form.is_valid() : # form.py의 clean 호출
            user=User(
                user_id = register_form.user_id,
                user_pw = register_form.user_pw,
                user_name = register_form.user_name,
                user_email = register_form.user_email
            )
            user.save()
            return redirect('/')
        else : 
            context['forms'] = register_form
            if register_form.errors : 
                for value in register_form.errors.values() :
                    context['error'] = value
        return render(request, 'users/register.html', context)

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

    if request.method == "GET":
        return redirect('smartfarm:main')

    elif request.method == "POST":
        login_user_id=request.POST['user_id']
        login_user_pw = request.POST['user_pw']

        try:
            user = User.objects.get(user_id=login_user_id)
        except User.DoesNotExist:
            user=None
            result = {
                'result':'success',
                'data' : "fail"
            }
            return JsonResponse(result)
        
        try :
            PasswordHasher().verify(user.user_pw.encode(), login_user_pw.encode())
        except exceptions.VerifyMismatchError:
            user=None  
        
        if user != None:
            request.session['user'] = user.id
            result = {
                'result':'success',
                'data' : "cor"
            }
            # Redirect to a success page.
            return JsonResponse(result)
            
        else:
            result = {
                'result':'success',
                'data' : "fail"
            }
            return JsonResponse(result)

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
